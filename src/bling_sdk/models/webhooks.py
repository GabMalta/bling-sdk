"""Webhook event models.

Payload shapes are transcribed from the version-1 examples in Bling's webhook docs. Every
``deleted`` action carries only ``{"id": N}``, whatever the resource.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import BlingModel, Data, DataHora, Ref


class PayloadExcluido(BlingModel):
    """Every ``deleted`` event, for every resource."""

    id: int | None = None


class PedidoVendaWebhook(BlingModel):
    id: int | None = None
    data: Data | None = None
    numero: int | None = None
    numero_loja: str | None = None
    total: float | None = None
    contato: Ref | None = None
    vendedor: Ref | None = None
    loja: Ref | None = None
    #: ``{"id": N, "valor": N}`` -- `valor` is the numeric status used on the order.
    situacao: BlingModel | None = None


class ProdutoWebhook(BlingModel):
    id: int | None = None
    nome: str | None = None
    codigo: str | None = None
    tipo: str | None = None
    situacao: str | None = None
    preco: float | None = None
    unidade: str | None = None
    formato: str | None = None
    id_produto_pai: int | None = None
    categoria: Ref | None = None
    descricao_curta: str | None = None
    descricao_complementar: str | None = None


class DepositoEstoqueWebhook(BlingModel):
    id: int | None = None
    saldo_fisico: float | None = None
    saldo_virtual: float | None = None


class EstoqueWebhook(BlingModel):
    """Fired by **physical** movements only: sales, NF-e, the stock screen.

    ``operacao`` is absent on a ``deleted`` event.
    """

    produto: Ref | None = None
    deposito: DepositoEstoqueWebhook | None = None
    operacao: str | None = None
    quantidade: float | None = None
    saldo_fisico_total: float | None = None
    saldo_virtual_total: float | None = None


class EstoqueVirtualWebhook(BlingModel):
    """Fired by sales reservations and by composition/virtual-stock recalculation.

    Enabled automatically when the stock webhook is, and inherits its configuration.
    """

    produto: Ref | None = None
    saldo_fisico_total: float | None = None
    saldo_virtual_total: float | None = None
    #: True when more than 200 linked products (components or compositions) had their
    #: virtual stock updated. The payload then omits them and the balances must be
    #: re-fetched with ``client.estoques.saldos(...)``.
    vinculo_complexo: bool | None = None
    depositos: list[DepositoEstoqueWebhook] = Field(default_factory=list)


class ProdutoFornecedorWebhook(BlingModel):
    id: int | None = None
    descricao: str | None = None
    codigo: str | None = None
    preco_custo: float | None = None
    preco_compra: float | None = None
    padrao: bool | None = None
    garantia: int | None = None
    produto: Ref | None = None
    fornecedor: Ref | None = None


class NotaFiscalWebhook(BlingModel):
    """Shared by the ``invoice`` and ``consumer_invoice`` resources."""

    id: int | None = None
    tipo: int | None = None
    situacao: int | None = None
    numero: str | None = None
    data_emissao: DataHora | None = None
    data_operacao: DataHora | None = None
    contato: Ref | None = None
    natureza_operacao: Ref | None = None
    loja: Ref | None = None


class EventoWebhook(BlingModel):
    """The envelope every webhook arrives in.

    Delivery is **not ordered** and **not deduplicated**: an ``updated`` can arrive before
    the ``created`` for the same record, and the same ``event_id`` can arrive twice. Key
    idempotency on ``event_id`` and process asynchronously.
    """

    event_id: str
    date: DataHora
    version: str = "v1"
    #: ``"$resource.$action"``, e.g. ``"product.updated"``.
    event: str
    #: A 32-character hash, **not** an int. This is the multi-company routing key.
    company_id: str
    data: dict[str, Any] = Field(default_factory=dict)

    @property
    def recurso(self) -> str:
        return self.event.split(".", 1)[0]

    @property
    def acao(self) -> str:
        partes = self.event.split(".", 1)
        return partes[1] if len(partes) > 1 else ""

    def payload(self) -> BlingModel:
        """Parse ``data`` into the model matching this resource and action."""
        if self.acao == "deleted":
            return PayloadExcluido.model_validate(self.data)
        modelo = _POR_RECURSO.get(self.recurso)
        if modelo is None:
            return BlingModel.model_validate(self.data)
        return modelo.model_validate(self.data)


_POR_RECURSO: dict[str, type[BlingModel]] = {
    "order": PedidoVendaWebhook,
    "product": ProdutoWebhook,
    "stock": EstoqueWebhook,
    "virtual_stock": EstoqueVirtualWebhook,
    "product_supplier": ProdutoFornecedorWebhook,
    "invoice": NotaFiscalWebhook,
    "consumer_invoice": NotaFiscalWebhook,
}
