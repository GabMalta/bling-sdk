"""Base machinery for the API resource groups.

Method naming is load-bearing, because PUT in Bling destroys data:

===========================  ==========================================  ================
Bling                        method                                      guard
===========================  ==========================================  ================
``GET /x``                   ``listar()``, ``iter_todos()``              --
``GET /x/{id}``              ``obter(id)``                               --
``POST /x``                  ``criar(dados)``                            not idempotent
``PATCH /x/{id}``            ``atualizar_parcial(id, dados)``            --
``PUT /x/{id}``              ``substituir(id, dados, confirmar=True)``   raises without it
``DELETE /x/{id}``           ``excluir(id)``                             --
``DELETE /x``                ``excluir_muitos(ids)``                     --
===========================  ==========================================  ================

There is deliberately **no method named ``atualizar``**. A caller who types
``.atualizar(id, {"preco": 9.9})`` gets an ``AttributeError`` naming the two real options,
rather than a silent PUT that wipes ``descricaoCurta``, ``marca``, ``tributacao`` and every
custom field. Leaving the obvious short name unbound is what makes the footgun unreachable.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Any, Protocol

from pydantic import BaseModel

from ..config import LIMITE_PADRAO
from ..errors import BlingSubstituicaoNaoConfirmada
from ..models import BlingModel
from ..pagination import iter_paginas


class _Requester(Protocol):
    def request(
        self,
        metodo: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = ...,
        json: Any | None = ...,
        modelo: type[BaseModel] | None = ...,
        lista_de: type[BaseModel] | None = ...,
        idempotente: bool | None = ...,
        headers: Mapping[str, str] | None = ...,
        bruto: bool = ...,
        timeout: float | None = ...,
    ) -> Any: ...


def corpo(dados: BaseModel | Mapping[str, Any]) -> Any:
    """The one place a model becomes a wire body.

    Delegates to ``BlingModel.bruto()`` (camelCase aliases, unset fields omitted). A plain
    dict is passed through untouched -- it is already wire-shaped, which is what makes
    ``client.request()`` predictable.
    """
    if isinstance(dados, BlingModel):
        return dados.bruto()
    if isinstance(dados, BaseModel):
        return dados.model_dump(by_alias=True, exclude_unset=True)
    return dict(dados)


def exigir_confirmacao(confirmar: bool, metodo: str, path: str) -> None:
    if not confirmar:
        raise BlingSubstituicaoNaoConfirmada(
            f"{metodo} {path} substitui o recurso INTEIRO: todo campo que voce nao enviar "
            "sera apagado ou zerado, sem recuperacao. Se e isso que voce quer, passe "
            "confirmar=True. Se voce so quer mudar alguns campos, use atualizar_parcial() "
            "quando o endpoint tiver PATCH, ou leia com obter(), altere o objeto e mande o "
            "objeto completo de volta."
        )


class Recurso:
    """Base for an API group.

    ``prefixo`` is the path segment, e.g. ``"produtos"``. Subresources set a nested prefix
    like ``"produtos/lojas"`` so the Python attribute path mirrors the URL.
    """

    prefixo: str = ""

    def __init__(self, client: _Requester) -> None:
        self._c = client

    # ---------------------------------------------------------------- paths

    def _path(self, *partes: Any) -> str:
        segmentos = [self.prefixo, *(str(p).strip("/") for p in partes if p is not None)]
        return "/".join(s for s in segmentos if s)

    # ---------------------------------------------------------------- verbs

    def _get(
        self,
        path: str,
        params: Mapping[str, Any] | None = None,
        *,
        modelo: type[BaseModel] | None = None,
        lista_de: type[BaseModel] | None = None,
        bruto: bool = False,
    ) -> Any:
        return self._c.request(
            "GET", path, params=params, modelo=modelo, lista_de=lista_de, bruto=bruto
        )

    def _post(
        self,
        path: str,
        json: Any | None = None,
        *,
        modelo: type[BaseModel] | None = None,
        params: Mapping[str, Any] | None = None,
        idempotente: bool | None = None,
    ) -> Any:
        return self._c.request(
            "POST", path, json=json, params=params, modelo=modelo, idempotente=idempotente
        )

    def _put(
        self,
        path: str,
        json: Any | None = None,
        *,
        modelo: type[BaseModel] | None = None,
    ) -> Any:
        return self._c.request("PUT", path, json=json, modelo=modelo)

    def _patch(
        self,
        path: str,
        json: Any | None = None,
        *,
        modelo: type[BaseModel] | None = None,
    ) -> Any:
        return self._c.request("PATCH", path, json=json, modelo=modelo)

    def _delete(self, path: str, params: Mapping[str, Any] | None = None) -> Any:
        return self._c.request("DELETE", path, params=params)

    # ---------------------------------------------------------------- listing

    def _listar(
        self,
        path: str,
        *,
        pagina: int = 1,
        limite: int = LIMITE_PADRAO,
        lista_de: type[BaseModel] | None = None,
        **filtros: Any,
    ) -> Any:
        """Exactly one HTTP call. What you reach for in a web view."""
        params = {"pagina": pagina, "limite": limite, **filtros}
        return self._get(path, params, lista_de=lista_de)

    def _iterar(
        self,
        path: str,
        *,
        limite: int = LIMITE_PADRAO,
        max_paginas: int | None = None,
        lista_de: type[BaseModel] | None = None,
        **filtros: Any,
    ) -> Iterator[Any]:
        """Lazy, pages internally. Does not accept ``pagina`` -- it owns it."""

        def buscar(*, pagina: int, limite: int, **extra: Any) -> list[Any]:
            resultado = self._listar(
                path, pagina=pagina, limite=limite, lista_de=lista_de, **extra
            )
            return resultado if isinstance(resultado, list) else []

        return iter_paginas(buscar, limite=limite, max_paginas=max_paginas, **filtros)
