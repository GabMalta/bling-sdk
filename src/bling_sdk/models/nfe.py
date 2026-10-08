"""Electronic invoice (NF-e) models.

``enviar()`` transmits to Sefaz and **cannot be undone**. There is no ``DELETE /nfe/{id}``
either -- Bling only exposes a collection delete, which is why ``Nfe`` has
``excluir_muitas()`` and no ``excluir()``.
"""

from __future__ import annotations

from pydantic import Field

from .common import BlingModel, Data, DataHora, Ref


class ItemNota(BlingModel):
    codigo: str | None = None
    descricao: str | None = None
    unidade: str | None = None
    quantidade: float | None = None
    valor: float | None = None
    tipo: str | None = None
    peso_bruto: float | None = None
    classificacao_fiscal: str | None = None
    cest: str | None = None
    origem: int | None = None
    produto: Ref | None = None


class ParcelaNota(BlingModel):
    data_vencimento: Data | None = None
    valor: float | None = None
    observacoes: str | None = None
    forma_pagamento: Ref | None = None


class VolumeNota(BlingModel):
    quantidade: int | None = None
    especie: str | None = None
    marca: str | None = None
    numeracao: str | None = None
    peso_bruto: float | None = None
    peso_liquido: float | None = None


class TransporteNota(BlingModel):
    #: 0 emitente, 1 destinatario, 2 terceiros, 9 sem frete.
    frete_por_conta: int | None = None
    frete: float | None = None
    transportador: Ref | None = None
    volumes: list[VolumeNota] = Field(default_factory=list)


class Intermediador(BlingModel):
    """Marketplace intermediary -- required on marketplace sales."""

    cnpj: str | None = None
    nome_usuario: str | None = None


class NotaFiscal(BlingModel):
    """``tipo``: 0 entrada, 1 saida. ``situacao`` is Bling's numeric invoice status.

    ``link_danfe`` and ``link_pdf`` carry an ``accessKey`` query parameter, so treat them as
    credentials -- do not log them.
    """

    id: int | None = None
    tipo: int | None = None
    situacao: int | None = None
    numero: str | None = None
    serie: str | None = None
    chave_acesso: str | None = None
    data_emissao: DataHora | None = None
    data_operacao: DataHora | None = None
    #: 1 normal, 2 complementar, 3 ajuste, 4 devolucao.
    finalidade: int | None = None
    tipo_nota: str | None = None
    valor_nota: float | None = None
    xml: str | None = None
    link_danfe: str | None = None
    link_pdf: str | None = None
    contato: Ref | None = None
    natureza_operacao: Ref | None = None
    loja: Ref | None = None
    vendedor: Ref | None = None
    intermediador: Intermediador | None = None
    transporte: TransporteNota | None = None
    itens: list[ItemNota] = Field(default_factory=list)
    parcelas: list[ParcelaNota] = Field(default_factory=list)
