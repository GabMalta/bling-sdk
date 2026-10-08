"""Sales order models.

``/pedidos/vendas`` has no PATCH: the only update is PUT, so changing one field means
reading the order, mutating it and sending the whole thing back via
``substituir(..., confirmar=True)``.
"""

from __future__ import annotations

from pydantic import Field

from .common import BlingModel, Data, Ref


class ItemPedido(BlingModel):
    id: int | None = None
    codigo: str | None = None
    unidade: str | None = None
    quantidade: float | None = None
    desconto: float | None = None
    valor: float | None = None
    aliquota_ipi: float | None = None
    descricao: str | None = None
    descricao_detalhada: str | None = None
    produto: Ref | None = None
    comissao: BlingModel | None = None


class Parcela(BlingModel):
    id: int | None = None
    data_vencimento: Data | None = None
    valor: float | None = None
    observacoes: str | None = None
    forma_pagamento: Ref | None = None


class Desconto(BlingModel):
    valor: float | None = None
    #: "R" for reais or "P" for percent.
    unidade: str | None = None


class Volume(BlingModel):
    id: int | None = None
    servico: str | None = None
    codigo_rastreamento: str | None = None


class Etiqueta(BlingModel):
    nome: str | None = None
    endereco: str | None = None
    numero: str | None = None
    complemento: str | None = None
    municipio: str | None = None
    uf: str | None = None
    cep: str | None = None
    bairro: str | None = None
    nome_pais: str | None = None


class Transporte(BlingModel):
    frete_por_conta: int | None = None
    frete: float | None = None
    quantidade_volumes: int | None = None
    peso_bruto: float | None = None
    prazo_entrega: int | None = None
    contato: Ref | None = None
    etiqueta: Etiqueta | None = None
    volumes: list[Volume] = Field(default_factory=list)


class Taxas(BlingModel):
    taxa_comissao: float | None = None
    custo_frete: float | None = None
    valor_base: float | None = None


class PedidoVenda(BlingModel):
    id: int | None = None
    numero: int | None = None
    numero_loja: str | None = None
    data: Data | None = None
    data_saida: Data | None = None
    data_prevista: Data | None = None
    total_produtos: float | None = None
    total: float | None = None
    contato: Ref | None = None
    situacao: Ref | None = None
    loja: Ref | None = None
    vendedor: Ref | None = None
    categoria: Ref | None = None
    id_unidade_negocio: int | None = None
    observacoes: str | None = None
    observacoes_internas: str | None = None
    desconto: Desconto | None = None
    tributacao: BlingModel | None = None
    transporte: Transporte | None = None
    taxas: Taxas | None = None
    itens: list[ItemPedido] = Field(default_factory=list)
    parcelas: list[Parcela] = Field(default_factory=list)
