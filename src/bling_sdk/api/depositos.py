"""``/depositos`` -- warehouses."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Any

from ..config import LIMITE_PADRAO
from ..models import Deposito
from ._base import Recurso, corpo, exigir_confirmacao


class Depositos(Recurso):
    """``/depositos``."""

    prefixo = "depositos"

    def listar(
        self,
        *,
        pagina: int = 1,
        limite: int = LIMITE_PADRAO,
        situacao: int | None = None,
        **filtros: Any,
    ) -> Any:
        """GET /depositos -> list[Deposito]. One HTTP call."""
        return self._listar(
            self.prefixo,
            pagina=pagina,
            limite=limite,
            lista_de=Deposito,
            situacao=situacao,
            **filtros,
        )

    def iter_todos(
        self, *, limite: int = LIMITE_PADRAO, max_paginas: int | None = None, **filtros: Any
    ) -> Iterator[Any]:
        return self._iterar(
            self.prefixo, limite=limite, max_paginas=max_paginas, lista_de=Deposito, **filtros
        )

    def obter(self, id_deposito: int) -> Any:
        """GET /depositos/{idDeposito} -> Deposito."""
        return self._get(self._path(id_deposito), modelo=Deposito)

    def criar(self, dados: Deposito | Mapping[str, Any]) -> Any:
        """POST /depositos -> Deposito."""
        return self._post(self.prefixo, corpo(dados), modelo=Deposito)

    def substituir(
        self, id_deposito: int, dados: Deposito | Mapping[str, Any], *, confirmar: bool = False
    ) -> Any:
        """PUT /depositos/{idDeposito} -- replaces the whole warehouse. No PATCH exists."""
        exigir_confirmacao(confirmar, "PUT", self._path(id_deposito))
        return self._put(self._path(id_deposito), corpo(dados), modelo=Deposito)
