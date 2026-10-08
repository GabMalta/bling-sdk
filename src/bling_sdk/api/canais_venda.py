"""``/canais-venda`` -- sales channels (marketplaces and stores). Read-only in the API."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from ..config import LIMITE_PADRAO
from ._base import Recurso


class CanaisVenda(Recurso):
    """``/canais-venda``.

    No model: the payload is small and its shape has not been pinned against a real response
    yet, so the raw ``data`` dict is returned.
    """

    prefixo = "canais-venda"

    def listar(self, *, pagina: int = 1, limite: int = LIMITE_PADRAO, **filtros: Any) -> Any:
        """GET /canais-venda -> list[dict]. One HTTP call."""
        return self._listar(self.prefixo, pagina=pagina, limite=limite, **filtros)

    def iter_todos(
        self, *, limite: int = LIMITE_PADRAO, max_paginas: int | None = None, **filtros: Any
    ) -> Iterator[Any]:
        return self._iterar(self.prefixo, limite=limite, max_paginas=max_paginas, **filtros)

    def obter(self, id_canal: int) -> Any:
        """GET /canais-venda/{idCanalVenda} -> dict."""
        return self._get(self._path(id_canal))

    def tipos(self) -> Any:
        """GET /canais-venda/tipos -> list[dict]. The channel types Bling supports."""
        return self._get(self._path("tipos"))
