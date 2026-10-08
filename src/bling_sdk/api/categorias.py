"""``/categorias`` -- only ``.produtos`` is modelled.

``/categorias/lojas`` and ``/categorias/receitas-despesas`` are reachable through
``client.request()`` and are each one more class.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Any

from ..config import LIMITE_PADRAO
from ..models import CategoriaProduto
from ._base import Recurso, corpo, exigir_confirmacao


class CategoriasProdutos(Recurso):
    """``/categorias/produtos``."""

    prefixo = "categorias/produtos"

    def listar(self, *, pagina: int = 1, limite: int = LIMITE_PADRAO, **filtros: Any) -> Any:
        """GET /categorias/produtos -> list[CategoriaProduto]. One HTTP call."""
        return self._listar(
            self.prefixo, pagina=pagina, limite=limite, lista_de=CategoriaProduto, **filtros
        )

    def iter_todas(
        self, *, limite: int = LIMITE_PADRAO, max_paginas: int | None = None, **filtros: Any
    ) -> Iterator[Any]:
        return self._iterar(
            self.prefixo,
            limite=limite,
            max_paginas=max_paginas,
            lista_de=CategoriaProduto,
            **filtros,
        )

    def obter(self, id_categoria: int) -> Any:
        """GET /categorias/produtos/{idCategoriaProduto} -> CategoriaProduto."""
        return self._get(self._path(id_categoria), modelo=CategoriaProduto)

    def criar(self, dados: CategoriaProduto | Mapping[str, Any]) -> Any:
        """POST /categorias/produtos -> CategoriaProduto."""
        return self._post(self.prefixo, corpo(dados), modelo=CategoriaProduto)

    def substituir(
        self,
        id_categoria: int,
        dados: CategoriaProduto | Mapping[str, Any],
        *,
        confirmar: bool = False,
    ) -> Any:
        """PUT /categorias/produtos/{idCategoriaProduto}. No PATCH exists."""
        exigir_confirmacao(confirmar, "PUT", self._path(id_categoria))
        return self._put(self._path(id_categoria), corpo(dados), modelo=CategoriaProduto)

    def excluir(self, id_categoria: int) -> Any:
        """DELETE /categorias/produtos/{idCategoriaProduto}."""
        return self._delete(self._path(id_categoria))


class Categorias:
    """Namespace mirroring ``/categorias``. Today only ``.produtos``."""

    def __init__(self, client: Any) -> None:
        self.produtos = CategoriasProdutos(client)
