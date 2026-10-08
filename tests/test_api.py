"""Uma tabela de (chamada -> verbo, path) sobre TODO metodo de recurso.

Barato de manter e e o unico teste que pega um path digitado errado antes de producao. Os
paths vem de reference/ENDPOINTS.md, extraido da doc oficial com verbo e operationId.
"""

import httpx
import pytest
import respx

from bling_sdk import BlingSubstituicaoNaoConfirmada
from conftest import HOST

# (id, lambda cliente, verbo, path esperado)
CHAMADAS = [
    # --- produtos -------------------------------------------------------------------------
    ("produtos.listar", lambda c: c.produtos.listar(), "GET", "/produtos"),
    ("produtos.obter", lambda c: c.produtos.obter(1), "GET", "/produtos/1"),
    ("produtos.criar", lambda c: c.produtos.criar({"nome": "x"}), "POST", "/produtos"),
    (
        "produtos.atualizar_parcial",
        lambda c: c.produtos.atualizar_parcial(1, {"preco": 9.9}),
        "PATCH",
        "/produtos/1",
    ),
    (
        "produtos.substituir",
        lambda c: c.produtos.substituir(1, {"nome": "x"}, confirmar=True),
        "PUT",
        "/produtos/1",
    ),
    ("produtos.excluir", lambda c: c.produtos.excluir(1), "DELETE", "/produtos/1"),
    ("produtos.excluir_muitos", lambda c: c.produtos.excluir_muitos([1, 2]), "DELETE", "/produtos"),
    (
        "produtos.alterar_situacao",
        lambda c: c.produtos.alterar_situacao(1, "I"),
        "PATCH",
        "/produtos/1/situacoes",
    ),
    (
        "produtos.alterar_situacoes",
        lambda c: c.produtos.alterar_situacoes([1, 2], "I"),
        "POST",
        "/produtos/situacoes",
    ),
    # --- produtos.variacoes ---------------------------------------------------------------
    (
        "variacoes.obter_por_pai",
        lambda c: c.produtos.variacoes.obter_por_pai(5),
        "GET",
        "/produtos/variacoes/5",
    ),
    (
        "variacoes.gerar_combinacoes",
        lambda c: c.produtos.variacoes.gerar_combinacoes({"atributos": []}),
        "POST",
        "/produtos/variacoes/atributos/gerar-combinacoes",
    ),
    (
        "variacoes.renomear_atributos",
        lambda c: c.produtos.variacoes.renomear_atributos(5, {"nome": "Cor"}),
        "PATCH",
        "/produtos/variacoes/5/atributos",
    ),
    # --- produtos.estruturas --------------------------------------------------------------
    (
        "estruturas.obter",
        lambda c: c.produtos.estruturas.obter(3),
        "GET",
        "/produtos/estruturas/3",
    ),
    (
        "estruturas.substituir",
        lambda c: c.produtos.estruturas.substituir(3, {}, confirmar=True),
        "PUT",
        "/produtos/estruturas/3",
    ),
    (
        "estruturas.adicionar_componentes",
        lambda c: c.produtos.estruturas.adicionar_componentes(3, {"componentes": []}),
        "POST",
        "/produtos/estruturas/3/componentes",
    ),
    (
        "estruturas.atualizar_parcial_componente",
        lambda c: c.produtos.estruturas.atualizar_parcial_componente(3, 7, {"quantidade": 2}),
        "PATCH",
        "/produtos/estruturas/3/componentes/7",
    ),
    (
        "estruturas.excluir_componentes",
        lambda c: c.produtos.estruturas.excluir_componentes(3, [7]),
        "DELETE",
        "/produtos/estruturas/3/componentes",
    ),
    (
        "estruturas.excluir_muitas",
        lambda c: c.produtos.estruturas.excluir_muitas([1]),
        "DELETE",
        "/produtos/estruturas",
    ),
    # --- produtos.fornecedores ------------------------------------------------------------
    (
        "fornecedores.listar",
        lambda c: c.produtos.fornecedores.listar(),
        "GET",
        "/produtos/fornecedores",
    ),
    (
        "fornecedores.obter",
        lambda c: c.produtos.fornecedores.obter(4),
        "GET",
        "/produtos/fornecedores/4",
    ),
    (
        "fornecedores.criar",
        lambda c: c.produtos.fornecedores.criar({"codigo": "x"}),
        "POST",
        "/produtos/fornecedores",
    ),
    (
        "fornecedores.substituir",
        lambda c: c.produtos.fornecedores.substituir(4, {}, confirmar=True),
        "PUT",
        "/produtos/fornecedores/4",
    ),
    (
        "fornecedores.excluir",
        lambda c: c.produtos.fornecedores.excluir(4),
        "DELETE",
        "/produtos/fornecedores/4",
    ),
    # --- produtos.lojas -------------------------------------------------------------------
    ("lojas.listar", lambda c: c.produtos.lojas.listar(), "GET", "/produtos/lojas"),
    ("lojas.obter", lambda c: c.produtos.lojas.obter(6), "GET", "/produtos/lojas/6"),
    ("lojas.criar", lambda c: c.produtos.lojas.criar({"preco": 1}), "POST", "/produtos/lojas"),
    (
        "lojas.substituir",
        lambda c: c.produtos.lojas.substituir(6, {"preco": 2}, confirmar=True),
        "PUT",
        "/produtos/lojas/6",
    ),
    ("lojas.excluir", lambda c: c.produtos.lojas.excluir(6), "DELETE", "/produtos/lojas/6"),
    # --- estoques -------------------------------------------------------------------------
    ("estoques.saldos", lambda c: c.estoques.saldos(), "GET", "/estoques/saldos"),
    (
        "estoques.saldos_por_deposito",
        lambda c: c.estoques.saldos_por_deposito(10),
        "GET",
        "/estoques/saldos/10",
    ),
    ("estoques.criar", lambda c: c.estoques.criar({"quantidade": 1}), "POST", "/estoques"),
    (
        "estoques.lancar",
        lambda c: c.estoques.lancar(1, operacao="E", quantidade=5, id_deposito=10),
        "POST",
        "/estoques",
    ),
    (
        "estoques.substituir",
        lambda c: c.estoques.substituir(2, {}, confirmar=True),
        "PUT",
        "/estoques/2",
    ),
    # --- depositos ------------------------------------------------------------------------
    ("depositos.listar", lambda c: c.depositos.listar(), "GET", "/depositos"),
    ("depositos.obter", lambda c: c.depositos.obter(10), "GET", "/depositos/10"),
    ("depositos.criar", lambda c: c.depositos.criar({"descricao": "x"}), "POST", "/depositos"),
    (
        "depositos.substituir",
        lambda c: c.depositos.substituir(10, {}, confirmar=True),
        "PUT",
        "/depositos/10",
    ),
    # --- pedidos.vendas -------------------------------------------------------------------
    ("vendas.listar", lambda c: c.pedidos.vendas.listar(), "GET", "/pedidos/vendas"),
    ("vendas.obter", lambda c: c.pedidos.vendas.obter(9), "GET", "/pedidos/vendas/9"),
    ("vendas.criar", lambda c: c.pedidos.vendas.criar({"numero": 1}), "POST", "/pedidos/vendas"),
    (
        "vendas.substituir",
        lambda c: c.pedidos.vendas.substituir(9, {}, confirmar=True),
        "PUT",
        "/pedidos/vendas/9",
    ),
    ("vendas.excluir", lambda c: c.pedidos.vendas.excluir(9), "DELETE", "/pedidos/vendas/9"),
    (
        "vendas.excluir_muitos",
        lambda c: c.pedidos.vendas.excluir_muitos([9]),
        "DELETE",
        "/pedidos/vendas",
    ),
    (
        "vendas.alterar_situacao",
        lambda c: c.pedidos.vendas.alterar_situacao(9, 77),
        "PATCH",
        "/pedidos/vendas/9/situacoes/77",
    ),
    (
        "vendas.lancar_estoque",
        lambda c: c.pedidos.vendas.lancar_estoque(9),
        "POST",
        "/pedidos/vendas/9/lancar-estoque",
    ),
    (
        "vendas.lancar_estoque_deposito",
        lambda c: c.pedidos.vendas.lancar_estoque(9, 10),
        "POST",
        "/pedidos/vendas/9/lancar-estoque/10",
    ),
    (
        "vendas.estornar_estoque",
        lambda c: c.pedidos.vendas.estornar_estoque(9),
        "POST",
        "/pedidos/vendas/9/estornar-estoque",
    ),
    (
        "vendas.lancar_contas",
        lambda c: c.pedidos.vendas.lancar_contas(9),
        "POST",
        "/pedidos/vendas/9/lancar-contas",
    ),
    (
        "vendas.estornar_contas",
        lambda c: c.pedidos.vendas.estornar_contas(9),
        "POST",
        "/pedidos/vendas/9/estornar-contas",
    ),
    (
        "vendas.gerar_nfe",
        lambda c: c.pedidos.vendas.gerar_nfe(9),
        "POST",
        "/pedidos/vendas/9/gerar-nfe",
    ),
    (
        "vendas.gerar_nfce",
        lambda c: c.pedidos.vendas.gerar_nfce(9),
        "POST",
        "/pedidos/vendas/9/gerar-nfce",
    ),
    # --- contatos -------------------------------------------------------------------------
    ("contatos.listar", lambda c: c.contatos.listar(), "GET", "/contatos"),
    ("contatos.obter", lambda c: c.contatos.obter(8), "GET", "/contatos/8"),
    ("contatos.criar", lambda c: c.contatos.criar({"nome": "x"}), "POST", "/contatos"),
    (
        "contatos.substituir",
        lambda c: c.contatos.substituir(8, {}, confirmar=True),
        "PUT",
        "/contatos/8",
    ),
    ("contatos.excluir", lambda c: c.contatos.excluir(8), "DELETE", "/contatos/8"),
    ("contatos.excluir_muitos", lambda c: c.contatos.excluir_muitos([8]), "DELETE", "/contatos"),
    (
        "contatos.consumidor_final",
        lambda c: c.contatos.consumidor_final(),
        "GET",
        "/contatos/consumidor-final",
    ),
    ("contatos.tipos", lambda c: c.contatos.tipos(), "GET", "/contatos/tipos"),
    (
        "contatos.tipos_do_contato",
        lambda c: c.contatos.tipos_do_contato(8),
        "GET",
        "/contatos/8/tipos",
    ),
    (
        "contatos.alterar_situacao",
        lambda c: c.contatos.alterar_situacao(8, "I"),
        "PATCH",
        "/contatos/8/situacoes",
    ),
    (
        "contatos.alterar_situacoes",
        lambda c: c.contatos.alterar_situacoes([8], "I"),
        "POST",
        "/contatos/situacoes",
    ),
    # --- nfe ------------------------------------------------------------------------------
    ("nfe.listar", lambda c: c.nfe.listar(), "GET", "/nfe"),
    ("nfe.obter", lambda c: c.nfe.obter(11), "GET", "/nfe/11"),
    ("nfe.criar", lambda c: c.nfe.criar({"tipo": 1}), "POST", "/nfe"),
    ("nfe.substituir", lambda c: c.nfe.substituir(11, {}, confirmar=True), "PUT", "/nfe/11"),
    ("nfe.excluir_muitas", lambda c: c.nfe.excluir_muitas([11]), "DELETE", "/nfe"),
    ("nfe.enviar", lambda c: c.nfe.enviar(11), "POST", "/nfe/11/enviar"),
    ("nfe.lancar_contas", lambda c: c.nfe.lancar_contas(11), "POST", "/nfe/11/lancar-contas"),
    (
        "nfe.estornar_contas",
        lambda c: c.nfe.estornar_contas(11),
        "POST",
        "/nfe/11/estornar-contas",
    ),
    ("nfe.lancar_estoque", lambda c: c.nfe.lancar_estoque(11), "POST", "/nfe/11/lancar-estoque"),
    (
        "nfe.lancar_estoque_deposito",
        lambda c: c.nfe.lancar_estoque(11, 10),
        "POST",
        "/nfe/11/lancar-estoque/10",
    ),
    (
        "nfe.estornar_estoque",
        lambda c: c.nfe.estornar_estoque(11),
        "POST",
        "/nfe/11/estornar-estoque",
    ),
    (
        "nfe.obter_documento",
        lambda c: c.nfe.obter_documento("CHAVE123"),
        "GET",
        "/nfe/documento/CHAVE123",
    ),
    # --- situacoes ------------------------------------------------------------------------
    ("situacoes.modulos", lambda c: c.situacoes.modulos(), "GET", "/situacoes/modulos"),
    ("situacoes.do_modulo", lambda c: c.situacoes.do_modulo(2), "GET", "/situacoes/modulos/2"),
    (
        "situacoes.acoes_do_modulo",
        lambda c: c.situacoes.acoes_do_modulo(2),
        "GET",
        "/situacoes/modulos/2/acoes",
    ),
    (
        "situacoes.transicoes_do_modulo",
        lambda c: c.situacoes.transicoes_do_modulo(2),
        "GET",
        "/situacoes/modulos/2/transicoes",
    ),
    ("situacoes.obter", lambda c: c.situacoes.obter(3), "GET", "/situacoes/3"),
    ("situacoes.criar", lambda c: c.situacoes.criar({"nome": "x"}), "POST", "/situacoes"),
    (
        "situacoes.substituir",
        lambda c: c.situacoes.substituir(3, {}, confirmar=True),
        "PUT",
        "/situacoes/3",
    ),
    ("situacoes.excluir", lambda c: c.situacoes.excluir(3), "DELETE", "/situacoes/3"),
    (
        "transicoes.obter",
        lambda c: c.situacoes.transicoes.obter(4),
        "GET",
        "/situacoes/transicoes/4",
    ),
    (
        "transicoes.criar",
        lambda c: c.situacoes.transicoes.criar({}),
        "POST",
        "/situacoes/transicoes",
    ),
    (
        "transicoes.substituir",
        lambda c: c.situacoes.transicoes.substituir(4, {}, confirmar=True),
        "PUT",
        "/situacoes/transicoes/4",
    ),
    (
        "transicoes.excluir",
        lambda c: c.situacoes.transicoes.excluir(4),
        "DELETE",
        "/situacoes/transicoes/4",
    ),
    # --- categorias -----------------------------------------------------------------------
    (
        "categorias.produtos.listar",
        lambda c: c.categorias.produtos.listar(),
        "GET",
        "/categorias/produtos",
    ),
    (
        "categorias.produtos.obter",
        lambda c: c.categorias.produtos.obter(12),
        "GET",
        "/categorias/produtos/12",
    ),
    (
        "categorias.produtos.criar",
        lambda c: c.categorias.produtos.criar({"descricao": "x"}),
        "POST",
        "/categorias/produtos",
    ),
    (
        "categorias.produtos.substituir",
        lambda c: c.categorias.produtos.substituir(12, {}, confirmar=True),
        "PUT",
        "/categorias/produtos/12",
    ),
    (
        "categorias.produtos.excluir",
        lambda c: c.categorias.produtos.excluir(12),
        "DELETE",
        "/categorias/produtos/12",
    ),
    # --- canais-venda / empresas ----------------------------------------------------------
    ("canais_venda.listar", lambda c: c.canais_venda.listar(), "GET", "/canais-venda"),
    ("canais_venda.obter", lambda c: c.canais_venda.obter(13), "GET", "/canais-venda/13"),
    ("canais_venda.tipos", lambda c: c.canais_venda.tipos(), "GET", "/canais-venda/tipos"),
    (
        "empresas.dados_basicos",
        lambda c: c.empresas.dados_basicos(),
        "GET",
        "/empresas/me/dados-basicos",
    ),
    (
        "cliente.dados_empresa",
        lambda c: c.dados_empresa(),
        "GET",
        "/empresas/me/dados-basicos",
    ),
]


@respx.mock
@pytest.mark.parametrize(
    ("chamar", "verbo", "path"),
    [pytest.param(c, v, p, id=i) for i, c, v, p in CHAMADAS],
)
def test_verbo_e_path(cliente, chamar, verbo, path):
    # `{"data": {}}` serve aos dois casos: `modelo=` valida um objeto vazio (todo campo e
    # opcional) e `lista_de=` trata nao-lista como lista vazia.
    rota = respx.route(method=verbo, url=f"{HOST}{path}").respond(json={"data": {}})
    chamar(cliente)
    assert rota.call_count == 1, f"esperado {verbo} {path}"


def test_tabela_cobre_toda_a_superficie_publica(cliente):
    """Nenhum metodo publico de recurso deve ficar fora da tabela acima."""
    cobertos = {i for i, _, _, _ in CHAMADAS}
    faltando = []
    grupos = {
        "produtos": cliente.produtos,
        "variacoes": cliente.produtos.variacoes,
        "estruturas": cliente.produtos.estruturas,
        "fornecedores": cliente.produtos.fornecedores,
        "lojas": cliente.produtos.lojas,
        "estoques": cliente.estoques,
        "depositos": cliente.depositos,
        "vendas": cliente.pedidos.vendas,
        "contatos": cliente.contatos,
        "nfe": cliente.nfe,
        "situacoes": cliente.situacoes,
        "transicoes": cliente.situacoes.transicoes,
        "categorias.produtos": cliente.categorias.produtos,
        "canais_venda": cliente.canais_venda,
        "empresas": cliente.empresas,
    }
    for nome_grupo, grupo in grupos.items():
        for attr in dir(grupo):
            if attr.startswith("_") or attr.startswith("iter_") or attr == "prefixo":
                continue
            if not callable(getattr(grupo, attr)):
                continue
            if f"{nome_grupo}.{attr}" not in cobertos:
                faltando.append(f"{nome_grupo}.{attr}")
    assert faltando == [], f"metodos sem teste de path: {faltando}"


# --- guarda do PUT --------------------------------------------------------------------------

SUBSTITUICOES = [
    ("produtos", lambda c: c.produtos.substituir(1, {})),
    ("estruturas", lambda c: c.produtos.estruturas.substituir(1, {})),
    ("fornecedores", lambda c: c.produtos.fornecedores.substituir(1, {})),
    ("lojas", lambda c: c.produtos.lojas.substituir(1, {})),
    ("estoques", lambda c: c.estoques.substituir(1, {})),
    ("depositos", lambda c: c.depositos.substituir(1, {})),
    ("vendas", lambda c: c.pedidos.vendas.substituir(1, {})),
    ("contatos", lambda c: c.contatos.substituir(1, {})),
    ("nfe", lambda c: c.nfe.substituir(1, {})),
    ("situacoes", lambda c: c.situacoes.substituir(1, {})),
    ("transicoes", lambda c: c.situacoes.transicoes.substituir(1, {})),
    ("categorias", lambda c: c.categorias.produtos.substituir(1, {})),
]


@respx.mock
@pytest.mark.parametrize(
    "chamar", [pytest.param(f, id=i) for i, f in SUBSTITUICOES]
)
def test_substituir_sem_confirmar_nao_faz_http(cliente, chamar):
    with pytest.raises(BlingSubstituicaoNaoConfirmada, match="confirmar=True"):
        chamar(cliente)
    assert respx.calls.call_count == 0


@pytest.mark.parametrize(
    "grupo",
    ["produtos", "contatos", "depositos", "nfe", "situacoes"],
)
def test_nao_existe_metodo_atualizar(cliente, grupo):
    """`atualizar` fica deliberadamente sem binding: digitar isso levanta AttributeError.

    Se existisse e fosse PUT, uma chamada distraida apagaria tributacao, marca e campos
    customizados sem aviso.
    """
    recurso = getattr(cliente, grupo)
    assert not hasattr(recurso, "atualizar")


def test_recursos_sem_listar_nao_mentem(cliente):
    """Endpoints que o Bling nao expoe nao devem aparecer como metodo."""
    assert not hasattr(cliente.situacoes, "listar")  # nao existe GET /situacoes
    assert not hasattr(cliente.produtos.estruturas, "listar")  # nem GET /produtos/estruturas
    assert not hasattr(cliente.estoques, "obter")  # nem GET /estoques/{id}
    assert not hasattr(cliente.nfe, "excluir")  # nfe so tem delete de colecao


@respx.mock
def test_lancar_valida_operacao(cliente):
    with pytest.raises(ValueError, match="entrada"):
        cliente.estoques.lancar(1, operacao="X", quantidade=1)
    assert respx.calls.call_count == 0


@respx.mock
def test_lancar_monta_o_payload(cliente):
    rota = respx.post(f"{HOST}/estoques").respond(json={"data": {"id": 1}})
    cliente.estoques.lancar(7, operacao="S", quantidade=3.5, id_deposito=10, preco=9.9)
    import json as _json

    corpo = _json.loads(rota.calls[0].request.content)
    assert corpo == {
        "produto": {"id": 7},
        "operacao": "S",
        "quantidade": 3.5,
        "deposito": {"id": 10},
        "preco": 9.9,
    }


@respx.mock
def test_modelo_vira_corpo_camelcase(cliente):
    from bling_sdk.models import Produto

    rota = respx.post(f"{HOST}/produtos").respond(json={"data": {"id": 1}})
    cliente.produtos.criar(Produto(nome="Copo", descricao_curta="curta"))
    import json as _json

    assert _json.loads(rota.calls[0].request.content) == {
        "nome": "Copo",
        "descricaoCurta": "curta",
    }


@respx.mock
def test_excluir_muitos_manda_ids_como_array(cliente):
    rota = respx.delete(f"{HOST}/produtos").respond(json={"data": None})
    cliente.produtos.excluir_muitos([1, 2, 3])
    url = str(rota.calls[0].request.url)
    assert url.count("idsProdutos%5B%5D=") == 3


def test_httpx_response_nao_e_necessario_para_respx():
    """Guarda-chuva: garante que httpx esta importavel no modulo de teste."""
    assert httpx.Response is not None
