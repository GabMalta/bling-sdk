"""Product models.

Field names come from the real v3 payloads (derived from the schemas in the integration
this replaces, snake_cased). **Every field is optional and every default is ``None`` or an
empty factory.** The old schemas baked one company's data into the defaults --
``marca="Legitima Textil"``, ``categoria.id=2432774``, ``tributacao.ncm="5407.52.10"``,
``unidade="Mt"``, and a 140-line table of custom-field ids -- which silently rewrote any
product created through them. That belongs in caller config, not in a library.
"""

from __future__ import annotations

from pydantic import Field

from .common import BlingModel, Data, Ref


class Dimensoes(BlingModel):
    largura: float | None = None
    altura: float | None = None
    profundidade: float | None = None
    #: 0 m, 1 cm, 2 mm (per Bling's unit table).
    unidade_medida: int | None = None


class EstoqueProduto(BlingModel):
    """The ``estoque`` block inside a product -- thresholds and balances, not movements."""

    minimo: float | None = None
    maximo: float | None = None
    crossdocking: int | None = None
    localizacao: str | None = None
    saldo_virtual_total: float | None = None
    saldo_fisico_total: float | None = None


class GrupoProduto(BlingModel):
    id: int | None = None
    nome: str | None = None


class Tributacao(BlingModel):
    """Tax fields. The irregular acronyms need explicit aliases."""

    origem: int | None = None
    n_fci: str | None = Field(None, alias="nFCI")
    ncm: str | None = None
    cest: str | None = None
    codigo_lista_servicos: str | None = None
    sped_tipo_item: str | None = None
    codigo_item: str | None = None
    percentual_tributos: float | None = None
    valor_base_st_retencao: float | None = None
    valor_st_retencao: float | None = None
    valor_icms_substituto: float | None = Field(None, alias="valorICMSSubstituto")
    codigo_excecao_tipi: str | None = None
    classe_enquadramento_ipi: str | None = None
    valor_ipi_fixo: float | None = None
    codigo_selo_ipi: str | None = None
    valor_pis_fixo: float | None = None
    valor_cofins_fixo: float | None = None
    codigo_anp: str | None = Field(None, alias="codigoANP")
    descricao_anp: str | None = Field(None, alias="descricaoANP")
    percentual_glp: float | None = Field(None, alias="percentualGLP")
    percentual_gas_nacional: float | None = None
    percentual_gas_importado: float | None = None
    valor_partida: float | None = None
    tipo_armamento: int | None = None
    descricao_completa_armamento: str | None = None
    dados_adicionais: str | None = None
    grupo_produto: GrupoProduto | None = None


class ImagemExterna(BlingModel):
    link: str | None = None


class Imagens(BlingModel):
    externas: list[ImagemExterna] = Field(default_factory=list)
    internas: list[BlingModel] = Field(default_factory=list)


class Video(BlingModel):
    url: str | None = None


class Midia(BlingModel):
    video: Video | None = None
    imagens: Imagens | None = None


class CampoCustomizado(BlingModel):
    """One custom field value.

    The ids are account-specific. Discover them with
    ``client.request("GET", "campos-customizados")`` rather than hardcoding a table.
    """

    id_campo_customizado: int | None = None
    id_vinculo: int | None = None
    valor: str | float | int | bool | None = None
    item: str | None = None


class ComponenteEstrutura(BlingModel):
    id: int | None = None
    produto: Ref | None = None
    quantidade: float | None = None


class Estrutura(BlingModel):
    #: "F" fixed or "V" variable, per the product structure docs.
    tipo_estoque: str | None = None
    lancamento_estoque: str | None = None
    componentes: list[ComponenteEstrutura] = Field(default_factory=list)


class ProdutoPai(BlingModel):
    id: int | None = None
    clone_info: bool | None = None


class VariacaoInfo(BlingModel):
    """The ``variacao`` block present on a child product."""

    nome: str | None = None
    ordem: int | None = None
    produto_pai: ProdutoPai | None = None


class FornecedorProduto(BlingModel):
    """The ``fornecedor`` block inside a product payload."""

    id: int | None = None
    contato: Ref | None = None
    codigo: str | None = None
    preco_custo: float | None = None
    preco_compra: float | None = None
    padrao: bool | None = None


class Produto(BlingModel):
    """A product, a service, a variation parent or a variation child.

    ``formato`` tells which: ``S`` simple, ``V`` has variations, ``E`` composition.
    ``tipo`` is ``P`` product or ``S`` service. ``situacao`` is ``A`` active or ``I``
    inactive.
    """

    id: int | None = None
    nome: str | None = None
    codigo: str | None = None
    preco: float | None = None
    preco_custo: float | None = None
    tipo: str | None = None
    situacao: str | None = None
    formato: str | None = None
    #: Set on a variation child, pointing at its parent.
    id_produto_pai: int | None = None
    descricao_curta: str | None = None
    descricao_complementar: str | None = None
    descricao_embalagem_discreta: str | None = None
    data_validade: Data | None = None
    unidade: str | None = None
    peso_liquido: float | None = None
    peso_bruto: float | None = None
    volumes: int | None = None
    itens_por_caixa: int | None = None
    gtin: str | None = None
    gtin_embalagem: str | None = None
    #: "T" third-party or "P" own production.
    tipo_producao: str | None = None
    #: 0 unspecified, 1 new, 2 used.
    condicao: int | None = None
    frete_gratis: bool | None = None
    marca: str | None = None
    duns: str | None = None
    link_externo: str | None = None
    observacoes: str | None = None
    imagem_url: str | None = Field(None, alias="imagemURL")
    categoria: Ref | None = None
    estoque: EstoqueProduto | None = None
    #: "T", "S" or "N" -- only meaningful on a PUT.
    action_estoque: str | None = None
    dimensoes: Dimensoes | None = None
    tributacao: Tributacao | None = None
    midia: Midia | None = None
    linha_produto: Ref | None = None
    estrutura: Estrutura | None = None
    fornecedor: FornecedorProduto | None = None
    variacao: VariacaoInfo | None = None
    campos_customizados: list[CampoCustomizado] = Field(default_factory=list)
    variacoes: list[Produto] = Field(default_factory=list)
    #: Present on a variation child in some responses.
    nome_variacao: str | None = None


class ProdutoFornecedor(BlingModel):
    """A product/supplier link -- ``/produtos/fornecedores``."""

    id: int | None = None
    descricao: str | None = None
    codigo: str | None = None
    preco_custo: float | None = None
    preco_compra: float | None = None
    padrao: bool | None = None
    garantia: int | None = None
    produto: Ref | None = None
    fornecedor: Ref | None = None


class ProdutoLoja(BlingModel):
    """A product/store link -- ``/produtos/lojas``.

    The old schema validated that ``idProdutoLoja`` contained a space. That was a workaround
    for one marketplace, not a rule of the API, and is deliberately not reproduced.
    """

    id: int | None = None
    preco: float | None = None
    preco_promocional: float | None = None
    codigo: str | None = None
    id_produto_loja: str | None = None
    produto: Ref | None = None
    loja: Ref | None = None
    fornecedor_loja: Ref | None = None
    marca_loja: Ref | None = None
    categorias_produtos: list[Ref] = Field(default_factory=list)
    descricao_curta: str | None = None
    descricao_complementar: str | None = None


Produto.model_rebuild()
