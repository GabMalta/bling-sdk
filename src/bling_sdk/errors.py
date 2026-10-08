"""Exception hierarchy.

Bling always answers an error with ``{"error": {"type", "message", "description"}}`` and a
matching HTTP status. ``error_for`` turns that pair into the most specific class, keeping
the raw payload so a caller can inspect anything this mapping does not model.

Transport and local-state failures are deliberately *siblings* of ``BlingErroAPI``, not
children: ``except BlingErroAPI`` should mean "the server said no", never "the socket died".
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .redaction import redigir, redigir_texto


class BlingError(Exception):
    """Base class for every error raised by this SDK."""


class BlingErroAPI(BlingError):
    """Bling answered with an error envelope."""

    def __init__(
        self,
        tipo: str,
        mensagem: str,
        descricao: str = "",
        *,
        status_code: int | None = None,
        payload: Mapping[str, Any] | None = None,
        campos: Any = None,
        metodo: str = "",
        path: str = "",
    ) -> None:
        onde = f"{metodo} {path} -> " if metodo or path else ""
        detalhe = descricao or mensagem
        super().__init__(redigir_texto(f"{onde}{status_code} {tipo}: {detalhe}".strip()))
        self.tipo = tipo
        self.mensagem = mensagem
        self.descricao = descricao
        self.status_code = status_code
        #: The response body exactly as received, redacted. Never discarded.
        self.payload: dict[str, Any] = dict(redigir(dict(payload or {})))
        #: ``error.fields`` when a VALIDATION_ERROR names the offending fields.
        self.campos = campos
        self.metodo = metodo
        self.path = path


class BlingErroValidacao(BlingErroAPI):
    """400 -- VALIDATION_ERROR, MISSING_REQUIRED_FIELD_ERROR or UNKNOWN_ERROR."""


class BlingNaoAutenticado(BlingErroAPI):
    """401 -- the access token is invalid, expired or revoked."""


class BlingSemPermissao(BlingErroAPI):
    """403 -- the token is fine but the registered app lacks this resource's scope.

    Worth its own class because the fix is non-obvious from the raw 403: the scope does not
    come from this code (the authorize URL deliberately sends no ``scope``), it comes from
    the permissions ticked on the app in the Bling panel. This bit us once already when
    turning on stock posting: a perfect token, and the endpoint still refusing.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.args = (
            f"{self.metodo} {self.path} -> 403 insufficient_scope: o app cadastrado no Bling "
            "nao tem o escopo deste recurso. O escopo nao vem do codigo (a URL de autorizacao "
            "nao envia `scope`) -- vem das permissoes marcadas em Aplicativos -> seu app, no "
            "painel do Bling. Marque o escopo e rode `bling auth` de novo para reemitir o token "
            "com o escopo novo.",
        )


class BlingNaoEncontrado(BlingErroAPI):
    """404 -- the path does not exist, or the id does not exist in this account."""


class BlingLimiteExcedido(BlingErroAPI):
    """429 -- TOO_MANY_REQUESTS."""

    def __init__(
        self, *args: Any, limite: int | None = None, periodo: str = "", **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.limite = limite
        self.periodo = periodo


class BlingLimitePorSegundo(BlingLimiteExcedido):
    """429 with ``period == "second"`` -- retryable after a short wait."""


class BlingLimiteDiario(BlingLimiteExcedido):
    """429 with ``period == "day"`` -- the 120.000/day budget is gone.

    Never retried: parking threads for hours is worse than failing and letting the caller
    reschedule.
    """


class BlingErroServidor(BlingErroAPI):
    """5xx -- a failure on Bling's side. Retryable, but only for idempotent verbs."""


class BlingErroTransporte(BlingError):
    """Network failure, timeout, or a response body that is not valid JSON."""


class BlingSemToken(BlingError):
    """No token stored for this company. Run ``bling auth``."""


class BlingIntervaloInvalido(BlingError):
    """A date filter spans more than a year; Bling would answer 400."""


class BlingSubstituicaoNaoConfirmada(BlingError):
    """``substituir()`` was called without ``confirmar=True``."""


class BlingAssinaturaInvalida(BlingError):
    """A webhook's X-Bling-Signature-256 does not match the computed HMAC."""


# Fallback dispatch by ``error.type``, for the undocumented case of an error envelope
# arriving under a 2xx status. Status stays the primary key everywhere else.
_POR_TIPO: dict[str, type[BlingErroAPI]] = {
    "VALIDATION_ERROR": BlingErroValidacao,
    "MISSING_REQUIRED_FIELD_ERROR": BlingErroValidacao,
    "UNKNOWN_ERROR": BlingErroValidacao,
    "invalid_token": BlingNaoAutenticado,
    "insufficient_scope": BlingSemPermissao,
    "RESOURCE_NOT_FOUND": BlingNaoEncontrado,
    "SERVER_ERROR": BlingErroServidor,
}


def _inteiro(valor: Any) -> int | None:
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def error_for(
    status: int,
    payload: Mapping[str, Any] | None,
    metodo: str = "",
    path: str = "",
) -> BlingErroAPI:
    """Pick the most specific exception for an error response.

    Dispatches on ``status`` as the primary key with ``type`` as the tiebreak, so an
    undocumented ``type`` on a known status still lands in the right class.
    """
    bruto: Mapping[str, Any] = payload if isinstance(payload, Mapping) else {}
    erro = bruto.get("error")
    if not isinstance(erro, Mapping):
        erro = {}

    tipo = str(erro.get("type") or "")
    mensagem = str(erro.get("message") or "")
    descricao = str(erro.get("description") or "")
    comum: dict[str, Any] = {
        "status_code": status,
        "payload": bruto,
        "campos": erro.get("fields"),
        "metodo": metodo,
        "path": path,
    }

    if status == 401:
        return BlingNaoAutenticado(tipo or "invalid_token", mensagem, descricao, **comum)
    if status == 403:
        return BlingSemPermissao(tipo or "insufficient_scope", mensagem, descricao, **comum)
    if status == 404:
        return BlingNaoEncontrado(tipo or "RESOURCE_NOT_FOUND", mensagem, descricao, **comum)
    if status == 429:
        periodo = str(erro.get("period") or "")
        cls: type[BlingErroAPI]
        cls = BlingLimiteDiario if periodo == "day" else BlingLimitePorSegundo
        return cls(
            tipo or "TOO_MANY_REQUESTS",
            mensagem,
            descricao,
            limite=_inteiro(erro.get("limit")),
            periodo=periodo,
            **comum,
        )
    if status >= 500:
        return BlingErroServidor(tipo or "SERVER_ERROR", mensagem, descricao, **comum)
    if status >= 400:
        padrao = "VALIDATION_ERROR" if status == 400 else "UNKNOWN_ERROR"
        return BlingErroValidacao(tipo or padrao, mensagem, descricao, **comum)
    # A 2xx carrying an `error` key -- undocumented. Dispatch on the type so the caller
    # still catches the specific class, rather than silently degrading to the base.
    cls = _POR_TIPO.get(tipo, BlingErroAPI)
    return cls(tipo or "UNKNOWN_ERROR", mensagem, descricao, **comum)
