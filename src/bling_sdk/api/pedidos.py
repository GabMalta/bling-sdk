"""``/pedidos`` -- sales orders.

Only ``.vendas`` is modelled. ``/pedidos/compras`` is one more class plus one attribute, and
is reachable today via ``client.request("GET", "pedidos/compras")``.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from datetime import date
from typing import Any

from ..config import LIMITE_PADRAO
from ..models import PedidoVenda
from ._base import Recurso, corpo, exigir_confirmacao


class PedidosVendas(Recurso):
    """``/pedidos/vendas``.

    No PATCH exists for the order itself: the only update is :meth:`substituir`. To change
    just the status use :meth:`alterar_situacao`, which is a dedicated endpoint.
    """

    prefixo = "pedidos/vendas"

    def listar(
        self,
        *,
        pagina: int = 1,
        limite: int = LIMITE_PADRAO,
        id_contato: int | None = None,
        ids_situacoes: list[int] | None = None,
        data_inicial: date | str | None = None,
        data_final: date | str | None = None,
        data_alteracao_inicial: date | str | None = None,
        data_alteracao_final: date | str | None = None,
        data_prevista_inicial: date | str | None = None,
        data_prevista_final: date | str | None = None,
        numero: int | None = None,
        numero_loja: str | None = None,
        id_loja: int | None = None,
        id_vendedor: int | None = None,
        id_unidade_negocio: int | None = None,
        **filtros: Any,
    ) -> Any:
        """GET /pedidos/vendas -> list[PedidoVenda]. One HTTP call."""
        return self._listar(
            self.prefixo,
            pagina=pagina,
            limite=limite,
            lista_de=PedidoVenda,
            idContato=id_contato,
            idsSituacoes=ids_situacoes,
            dataInicial=data_inicial,
            dataFinal=data_final,
            dataAlteracaoInicial=data_alteracao_inicial,
            dataAlteracaoFinal=data_alteracao_final,
            dataPrevistaInicial=data_prevista_inicial,
            dataPrevistaFinal=data_prevista_final,
            numero=numero,
            numeroLoja=numero_loja,
            idLoja=id_loja,
            idVendedor=id_vendedor,
            idUnidadeNegocio=id_unidade_negocio,
            **filtros,
        )

    def iter_todos(
        self, *, limite: int = LIMITE_PADRAO, max_paginas: int | None = None, **filtros: Any
    ) -> Iterator[Any]:
        return self._iterar(
            self.prefixo, limite=limite, max_paginas=max_paginas, lista_de=PedidoVenda, **filtros
        )

    def obter(self, id_pedido: int) -> Any:
        """GET /pedidos/vendas/{idPedidoVenda} -> PedidoVenda."""
        return self._get(self._path(id_pedido), modelo=PedidoVenda)

    def criar(self, dados: PedidoVenda | Mapping[str, Any]) -> Any:
        """POST /pedidos/vendas -> PedidoVenda. Not idempotent; no 5xx retry."""
        return self._post(self.prefixo, corpo(dados), modelo=PedidoVenda)

    def substituir(
        self, id_pedido: int, dados: PedidoVenda | Mapping[str, Any], *, confirmar: bool = False
    ) -> Any:
        """PUT /pedidos/vendas/{idPedidoVenda} -- replaces the whole order.

        There is no PATCH here, so this is the only way to edit an order. The safe recipe:
        ``pedido = client.pedidos.vendas.obter(id)``, mutate it, then pass the object back --
        the model keeps every field it read, including ones this SDK does not model.
        """
        exigir_confirmacao(confirmar, "PUT", self._path(id_pedido))
        return self._put(self._path(id_pedido), corpo(dados), modelo=PedidoVenda)

    def excluir(self, id_pedido: int) -> Any:
        """DELETE /pedidos/vendas/{idPedidoVenda}."""
        return self._delete(self._path(id_pedido))

    def excluir_muitos(self, ids: list[int]) -> Any:
        """DELETE /pedidos/vendas -- removes several orders by id."""
        return self._delete(self.prefixo, {"idsPedidosVendas": ids})

    def alterar_situacao(self, id_pedido: int, id_situacao: int) -> Any:
        """PATCH /pedidos/vendas/{idPedidoVenda}/situacoes/{idSituacao}."""
        return self._patch(self._path(id_pedido, "situacoes", id_situacao))

    # -- acoes. Todas POST, nenhuma idempotente: repetir lanca de novo. -------------------

    def lancar_estoque(self, id_pedido: int, id_deposito: int | None = None) -> Any:
        """POST /pedidos/vendas/{id}/lancar-estoque[/{idDeposito}].

        Posts the order's stock movements. **Not idempotent** -- calling it twice posts the
        movements twice. Reads like a safe "action", is not one.
        """
        partes = [id_pedido, "lancar-estoque"]
        if id_deposito is not None:
            partes.append(id_deposito)
        return self._post(self._path(*partes))

    def estornar_estoque(self, id_pedido: int) -> Any:
        """POST /pedidos/vendas/{idPedidoVenda}/estornar-estoque."""
        return self._post(self._path(id_pedido, "estornar-estoque"))

    def lancar_contas(self, id_pedido: int) -> Any:
        """POST /pedidos/vendas/{idPedidoVenda}/lancar-contas. Not idempotent."""
        return self._post(self._path(id_pedido, "lancar-contas"))

    def estornar_contas(self, id_pedido: int) -> Any:
        """POST /pedidos/vendas/{idPedidoVenda}/estornar-contas."""
        return self._post(self._path(id_pedido, "estornar-contas"))

    def gerar_nfe(self, id_pedido: int) -> Any:
        """POST /pedidos/vendas/{idPedidoVenda}/gerar-nfe.

        Creates the invoice but does **not** transmit it -- that is ``client.nfe.enviar()``.
        """
        return self._post(self._path(id_pedido, "gerar-nfe"))

    def gerar_nfce(self, id_pedido: int) -> Any:
        """POST /pedidos/vendas/{idPedidoVenda}/gerar-nfce."""
        return self._post(self._path(id_pedido, "gerar-nfce"))


class Pedidos:
    """Namespace mirroring ``/pedidos``. Today only ``.vendas``."""

    def __init__(self, client: Any) -> None:
        self.vendas = PedidosVendas(client)
