"""Sans-IO core shared by the client.

Everything that does not touch the network lives here: request preparation, query
normalization, the one-year filter guard, response/error parsing. ``client.py`` only adds
the actual I/O.

Two rules keep this module honest, and an async client later depends on both:

* nothing here imports ``time.sleep`` or performs I/O;
* nothing here renames a key. camelCase aliasing is the models' job, so there is exactly
  one aliasing boundary (``api/_base.corpo``) and ``client.request()`` stays predictable.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel

from .config import (
    API_BASE,
    CABECALHO_JWT,
    FORMATO_DATA,
    FORMATO_DATA_HORA,
    INTERVALO_MAXIMO_FILTRO,
    USER_AGENT,
)
from .errors import BlingErroTransporte, BlingIntervaloInvalido, error_for
from .redaction import redigir_texto

M = TypeVar("M", bound=BaseModel)


@dataclass(frozen=True)
class Prepared:
    """A fully built request, ready to hand to any transport.

    ``idempotente`` lives here rather than in ``retry.py`` because it is a property of
    *this* request, not of the verb alone: ``POST /pedidos/vendas/{id}/lancar-estoque``
    must stay non-idempotent even though it reads like a repeatable "action".
    """

    method: str
    url: str
    params: dict[str, Any] | None
    json: Any | None
    data: dict[str, str] | None
    headers: dict[str, str]
    idempotente: bool


def _valor_de_query(valor: Any) -> Any:
    """Coerce one query value to what Bling expects."""
    if isinstance(valor, bool):
        return "true" if valor else "false"
    if isinstance(valor, Enum):
        return _valor_de_query(valor.value)
    if isinstance(valor, datetime):
        return valor.strftime(FORMATO_DATA_HORA)
    if isinstance(valor, date):
        return valor.strftime(FORMATO_DATA)
    if isinstance(valor, Decimal):
        return str(valor)
    return valor


def normalizar_params(params: Mapping[str, Any] | None) -> dict[str, Any] | None:
    """The single place a query value is coerced.

    Drops ``None``; renders bools, dates, datetimes, enums and Decimals; and gives
    list-valued keys the ``[]`` suffix Bling's array filters use, so httpx emits
    ``idsProdutos[]=1&idsProdutos[]=2``.
    """
    if not params:
        return None
    saida: dict[str, Any] = {}
    for chave, valor in params.items():
        if valor is None:
            continue
        if isinstance(valor, (list, tuple, set, frozenset)):
            itens = [_valor_de_query(v) for v in valor if v is not None]
            if not itens:
                continue
            saida[chave if chave.endswith("[]") else f"{chave}[]"] = itens
        else:
            saida[chave] = _valor_de_query(valor)
    return saida or None


def _como_data(valor: Any) -> date | None:
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    if isinstance(valor, str):
        for fmt in (FORMATO_DATA_HORA, FORMATO_DATA):
            try:
                return datetime.strptime(valor[: len(fmt) + 2].strip(), fmt).date()
            except ValueError:
                continue
    return None


def validar_intervalo_datas(params: Mapping[str, Any] | None) -> None:
    """Raise when a ``...Inicial`` / ``...Final`` pair spans more than a year.

    Lives here, not in the resource methods, so it also covers ``client.request()`` --
    which is exactly where ad-hoc reporting queries go, and therefore the path most likely
    to trip the rule.

    Errs permissive (366 days, not 365): the SDK must never refuse something Bling would
    have accepted. A genuinely too-wide range still surfaces as Bling's own 400.
    """
    if not params:
        return
    for chave, valor in params.items():
        if not chave.endswith("Inicial"):
            continue
        final = params.get(f"{chave[: -len('Inicial')]}Final")
        if final is None:
            continue
        inicio, fim = _como_data(valor), _como_data(final)
        if inicio is None or fim is None:
            continue
        if fim - inicio > INTERVALO_MAXIMO_FILTRO:
            raise BlingIntervaloInvalido(
                f"o filtro {chave}..{chave[: -len('Inicial')]}Final cobre "
                f"{(fim - inicio).days} dias; o Bling recusa intervalos acima de um ano "
                f"(HTTP 400). Use bling_sdk.fatiar_periodo({inicio!r}, {fim!r}) e faca uma "
                "chamada por fatia."
            )


class Core:
    """Builds requests and parses responses. Holds no connection and no clock."""

    def __init__(self, *, base_url: str = API_BASE, enable_jwt: bool = True) -> None:
        self.base_url = base_url.rstrip("/")
        self.enable_jwt = enable_jwt

    def url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def prepare(
        self,
        metodo: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any | None = None,
        access_token: str | None = None,
        headers: Mapping[str, str] | None = None,
        idempotente: bool | None = None,
    ) -> Prepared:
        verbo = metodo.upper()
        query = normalizar_params(params)
        validar_intervalo_datas(query)

        cabecalhos: dict[str, str] = {"Accept": "application/json", "User-Agent": USER_AGENT}
        if access_token:
            cabecalhos["Authorization"] = f"Bearer {access_token}"
        if json is not None:
            cabecalhos["Content-Type"] = "application/json"
        if self.enable_jwt:
            # Must be kept on every authenticated request, not only on /oauth/token,
            # or Bling stops honouring JWT auth for this app.
            cabecalhos[CABECALHO_JWT] = "1"
        if headers:
            cabecalhos.update(headers)

        return Prepared(
            method=verbo,
            url=self.url(path),
            params=query,
            json=json,
            data=None,
            headers=cabecalhos,
            idempotente=verbo != "POST" if idempotente is None else idempotente,
        )

    def prepare_oauth(
        self,
        url: str,
        corpo: Mapping[str, str],
        cabecalhos: Mapping[str, str],
    ) -> Prepared:
        """A form-encoded POST to the OAuth server.

        Marked idempotent: a refresh retried after a *network* error is worth attempting,
        because a successful-but-lost response burns the refresh token either way and the
        retry at least surfaces the real failure instead of a timeout.
        """
        return Prepared(
            method="POST",
            url=url,
            params=None,
            json=None,
            data=dict(corpo),
            headers=dict(cabecalhos),
            idempotente=True,
        )

    def parse(
        self,
        resp: httpx.Response,
        modelo: type[M] | None = None,
        lista_de: type[M] | None = None,
        *,
        bruto: bool = False,
        metodo: str = "",
        path: str = "",
    ) -> Any:
        """Turn a response into data, a model, or an exception.

        One unwrapping rule, no exceptions to it: the ``{"data": ...}`` envelope is always
        stripped. Returning the envelope from some methods and the payload from others is
        the single worst ergonomic defect in the code this SDK replaces.
        """
        if bruto:
            return resp
        if resp.status_code == 204 or not resp.content:
            if resp.status_code >= 400:
                raise error_for(resp.status_code, None, metodo, path)
            return None

        try:
            payload = resp.json()
        except ValueError as exc:
            if resp.status_code >= 400:
                # Most likely an edge/WAF response (an IP block) rather than the API.
                raise error_for(resp.status_code, None, metodo, path) from exc
            trecho = redigir_texto(resp.text[:500])
            raise BlingErroTransporte(
                f"{metodo} {path} -> resposta nao-JSON (HTTP {resp.status_code}): {trecho}"
            ) from exc

        tem_erro = isinstance(payload, Mapping) and payload.get("error")
        if resp.status_code >= 400 or tem_erro:
            raise error_for(resp.status_code, payload if isinstance(payload, Mapping) else None,
                            metodo, path)

        corpo = payload["data"] if isinstance(payload, Mapping) and "data" in payload else payload
        if lista_de is not None:
            itens = corpo if isinstance(corpo, list) else []
            return [lista_de.model_validate(i) for i in itens]
        if modelo is not None:
            return modelo.model_validate(corpo)
        return corpo
