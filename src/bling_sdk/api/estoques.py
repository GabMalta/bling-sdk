"""``/estoques`` -- balances and movements.

Note what is *not* here: there is no ``GET /estoques/{idEstoque}``, so no ``obter()``. Read
balances with :meth:`Estoques.saldos`.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from datetime import datetime
from typing import Any

from ..config import LIMITE_PADRAO
from ..models import Estoque, Saldo
from ._base import Recurso, corpo, exigir_confirmacao


class Estoques(Recurso):
    """``/estoques``."""

    prefixo = "estoques"

    def saldos(
        self,
        *,
        ids_produtos: list[int] | None = None,
        codigos: list[str] | None = None,
        pagina: int = 1,
        limite: int = LIMITE_PADRAO,
        **filtros: Any,
    ) -> Any:
        """GET /estoques/saldos -> list[Saldo]. Balances across every warehouse."""
        return self._listar(
            self._path("saldos"),
            pagina=pagina,
            limite=limite,
            lista_de=Saldo,
            idsProdutos=ids_produtos,
            codigos=codigos,
            **filtros,
        )

    def iter_saldos(
        self, *, limite: int = LIMITE_PADRAO, max_paginas: int | None = None, **filtros: Any
    ) -> Iterator[Any]:
        return self._iterar(
            self._path("saldos"),
            limite=limite,
            max_paginas=max_paginas,
            lista_de=Saldo,
            **filtros,
        )

    def saldos_por_deposito(
        self,
        id_deposito: int,
        *,
        ids_produtos: list[int] | None = None,
        codigos: list[str] | None = None,
        pagina: int = 1,
        limite: int = LIMITE_PADRAO,
        **filtros: Any,
    ) -> Any:
        """GET /estoques/saldos/{idDeposito} -> list[Saldo]. One warehouse only."""
        return self._listar(
            self._path("saldos", id_deposito),
            pagina=pagina,
            limite=limite,
            lista_de=Saldo,
            idsProdutos=ids_produtos,
            codigos=codigos,
            **filtros,
        )

    def iter_saldos_por_deposito(
        self,
        id_deposito: int,
        *,
        limite: int = LIMITE_PADRAO,
        max_paginas: int | None = None,
        **filtros: Any,
    ) -> Iterator[Any]:
        return self._iterar(
            self._path("saldos", id_deposito),
            limite=limite,
            max_paginas=max_paginas,
            lista_de=Saldo,
            **filtros,
        )

    def criar(self, dados: Estoque | Mapping[str, Any]) -> Any:
        """POST /estoques -> Estoque. Posts a stock movement.

        **The most dangerous call in this SDK.** It is not idempotent and is deliberately
        **not** retried on a 5xx or a timeout: Bling may have posted the movement and lost
        only the response, and a retry would post it twice -- inflating a balance in a way
        nobody notices for weeks.

        If a call raises :class:`~bling_sdk.errors.BlingErroTransporte` or
        :class:`~bling_sdk.errors.BlingErroServidor`, do **not** blindly re-run it. Read the
        balance back with :meth:`saldos` and decide.

        See :meth:`lancar` for a typed wrapper.
        """
        return self._post(self.prefixo, corpo(dados), modelo=Estoque)

    def lancar(
        self,
        id_produto: int,
        *,
        operacao: str,
        quantidade: float,
        id_deposito: int | None = None,
        preco: float | None = None,
        custo: float | None = None,
        observacoes: str | None = None,
        data: datetime | str | None = None,
    ) -> Any:
        """Post a stock movement with named arguments.

        ``operacao`` is ``"E"`` for an entry (balance goes up) or ``"S"`` for an exit (down).

        Carries every warning on :meth:`criar`: not idempotent, never retried on 5xx.
        """
        if operacao not in {"E", "S"}:
            raise ValueError('operacao deve ser "E" (entrada) ou "S" (saida)')
        payload: dict[str, Any] = {
            "produto": {"id": id_produto},
            "operacao": operacao,
            "quantidade": quantidade,
        }
        if id_deposito is not None:
            payload["deposito"] = {"id": id_deposito}
        for chave, valor in (
            ("preco", preco),
            ("custo", custo),
            ("observacoes", observacoes),
            ("data", data),
        ):
            if valor is not None:
                payload[chave] = valor
        return self.criar(payload)

    def substituir(
        self, id_estoque: int, dados: Estoque | Mapping[str, Any], *, confirmar: bool = False
    ) -> Any:
        """PUT /estoques/{idEstoque} -- replaces a movement. No PATCH exists."""
        exigir_confirmacao(confirmar, "PUT", self._path(id_estoque))
        return self._put(self._path(id_estoque), corpo(dados), modelo=Estoque)
