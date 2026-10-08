"""Contact models -- customers, suppliers, carriers and sales reps are all ``contatos``."""

from __future__ import annotations

from pydantic import Field

from .common import BlingModel, Data, Ref


class Endereco(BlingModel):
    endereco: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    cep: str | None = None
    municipio: str | None = None
    uf: str | None = None
    pais: str | None = None


class EnderecoGeral(BlingModel):
    """Bling splits a contact's addresses into the main one and the billing one."""

    geral: Endereco | None = None
    cobranca: Endereco | None = None


class TipoContato(BlingModel):
    id: int | None = None
    descricao: str | None = None


class DadosAdicionais(BlingModel):
    data_nascimento: Data | None = None
    sexo: str | None = None
    naturalidade: str | None = None


class FinanceiroContato(BlingModel):
    limite_credito: float | None = None
    condicao_pagamento: str | None = None
    categoria: Ref | None = None


class Contato(BlingModel):
    """``tipo`` is ``"F"`` (pessoa fisica) or ``"J"`` (pessoa juridica).

    ``situacao`` is ``"A"`` active, ``"I"`` inactive or ``"E"`` excluded -- note that moving
    a contact to excluded emits an ``updated`` webhook, not a ``deleted`` one.
    """

    id: int | None = None
    nome: str | None = None
    codigo: str | None = None
    situacao: str | None = None
    #: CPF or CNPJ, digits only in most responses.
    numero_documento: str | None = None
    #: "F" pessoa fisica, "J" pessoa juridica.
    tipo: str | None = None
    telefone: str | None = None
    celular: str | None = None
    fantasia: str | None = None
    rg: str | None = None
    orgao_emissor: str | None = None
    email: str | None = None
    email_nota_fiscal: str | None = None
    inscricao_estadual: str | None = None
    indicador_ie: int | None = None
    endereco: EnderecoGeral | None = None
    vendedor: Ref | None = None
    dados_adicionais: DadosAdicionais | None = None
    financeiro: FinanceiroContato | None = None
    pais: Ref | None = None
    tipos_contato: list[TipoContato] = Field(default_factory=list)
