import httpx
import pytest
import respx

from bling_sdk import (
    BlingClient,
    BlingErroTransporte,
    BlingErroValidacao,
    BlingNaoEncontrado,
    BlingSemPermissao,
    BlingSemToken,
    InMemoryTokenStore,
    SemLimite,
)
from bling_sdk.config import CABECALHO_JWT
from bling_sdk.models import Produto
from conftest import HOST, token

# --- contrato do construtor ---------------------------------------------------------------


@respx.mock
def test_construtor_nao_faz_io_nem_imprime(capsys, http):
    """Construir o cliente tem de ser gratuito e silencioso.

    O codigo que este SDK substitui renovava token na rede dentro do __init__, imprimia em
    stdout e podia travar num input(). respx sem rota nenhuma garante que nada saiu na rede.
    """
    BlingClient("cid", "csecret", empresa="t", token_store=InMemoryTokenStore(),
                rate_limiter=SemLimite(), http_client=http)
    saida = capsys.readouterr()
    assert saida.out == "" and saida.err == ""
    assert respx.calls.call_count == 0


def test_construtor_nao_escreve_no_disco(tmp_path, monkeypatch, http):
    monkeypatch.setenv("BLING_SDK_HOME", str(tmp_path / "config"))
    BlingClient("cid", "csecret", http_client=http)
    assert not (tmp_path / "config").exists()


def test_repr_nao_vaza_segredo(cliente):
    assert "csecret" not in repr(cliente)


# --- envelope e modelos --------------------------------------------------------------------


@respx.mock
def test_get_desembrulha_data_e_valida_modelo(cliente):
    respx.get(f"{HOST}/produtos/1").respond(
        json={"data": {"id": 1, "nome": "Copo", "descricaoCurta": "c", "campoNovo": "x"}}
    )
    p = cliente.produtos.obter(1)
    assert isinstance(p, Produto)
    assert (p.id, p.nome, p.descricao_curta) == (1, "Copo", "c")
    assert p.model_extra == {"campoNovo": "x"}


@respx.mock
def test_listar_faz_exatamente_uma_chamada(cliente):
    rota = respx.get(f"{HOST}/produtos").respond(json={"data": [{"id": 1}, {"id": 2}]})
    itens = cliente.produtos.listar(limite=2)
    assert [i.id for i in itens] == [1, 2]
    assert rota.call_count == 1
    q = rota.calls[0].request.url.params
    assert q["pagina"] == "1" and q["limite"] == "2"


@respx.mock
def test_headers_de_auth_e_jwt(cliente):
    rota = respx.get(f"{HOST}/produtos").respond(json={"data": []})
    cliente.produtos.listar()
    h = rota.calls[0].request.headers
    assert h["authorization"] == "Bearer tok"
    assert h[CABECALHO_JWT] == "1"


@respx.mock
def test_jwt_pode_ser_desligado(store, limiter, http):
    c = BlingClient("cid", "cs", empresa="t", token_store=store, rate_limiter=limiter,
                    enable_jwt=False, http_client=http)
    rota = respx.get(f"{HOST}/produtos").respond(json={"data": []})
    c.produtos.listar()
    assert CABECALHO_JWT not in rota.calls[0].request.headers
    c.close()


# --- escape hatch --------------------------------------------------------------------------


@respx.mock
def test_escape_hatch_alcanca_endpoint_nao_modelado(cliente):
    rota = respx.get(f"{HOST}/vendedores").respond(json={"data": [{"id": 9}]})
    assert cliente.request("GET", "vendedores") == [{"id": 9}]
    assert rota.call_count == 1


@respx.mock
def test_bruto_devolve_a_resposta(cliente):
    respx.get(f"{HOST}/nfe/documento/ABC").respond(200, content=b"%PDF-1.4")
    r = cliente.nfe.obter_documento("ABC", bruto=True)
    assert isinstance(r, httpx.Response)
    assert r.content == b"%PDF-1.4"


@respx.mock
def test_params_lista_viram_array(cliente):
    rota = respx.get(f"{HOST}/produtos").respond(json={"data": []})
    cliente.produtos.listar(ids_produtos=[1, 2])
    assert "idsProdutos%5B%5D=1&idsProdutos%5B%5D=2" in str(rota.calls[0].request.url)


# --- mapeamento de erro --------------------------------------------------------------------


@respx.mock
def test_404_vira_nao_encontrado(cliente):
    respx.get(f"{HOST}/produtos/7").respond(
        404, json={"error": {"type": "RESOURCE_NOT_FOUND", "message": "m", "description": "d"}}
    )
    with pytest.raises(BlingNaoEncontrado):
        cliente.produtos.obter(7)


@respx.mock
def test_403_vira_sem_permissao_com_mensagem_acionavel(cliente):
    respx.get(f"{HOST}/estoques/saldos").respond(
        403, json={"error": {"type": "insufficient_scope", "message": "m", "description": "d"}}
    )
    with pytest.raises(BlingSemPermissao, match="painel do Bling"):
        cliente.estoques.saldos()


@respx.mock
def test_400_vira_erro_de_validacao_com_campos(cliente):
    respx.post(f"{HOST}/produtos").respond(
        400,
        json={
            "error": {
                "type": "VALIDATION_ERROR",
                "message": "m",
                "description": "d",
                "fields": [{"nome": "obrigatorio"}],
            }
        },
    )
    with pytest.raises(BlingErroValidacao) as info:
        cliente.produtos.criar({"preco": 1})
    assert info.value.campos == [{"nome": "obrigatorio"}]


@respx.mock
def test_corpo_nao_json_em_200_vira_erro_de_transporte(cliente):
    respx.get(f"{HOST}/produtos").respond(200, content=b"<html>nope</html>")
    with pytest.raises(BlingErroTransporte, match="nao-JSON"):
        cliente.produtos.listar()


# --- token ---------------------------------------------------------------------------------


@respx.mock
def test_sem_token_levanta_antes_de_qualquer_http(cliente_sem_token):
    with pytest.raises(BlingSemToken, match="bling auth"):
        cliente_sem_token.produtos.listar()
    assert respx.calls.call_count == 0


@respx.mock
def test_duas_empresas_usam_tokens_distintos(limiter, http):
    store = InMemoryTokenStore()
    store.set("a", token("token-a"))
    store.set("b", token("token-b"))
    rota = respx.get(f"{HOST}/produtos").respond(json={"data": []})

    for empresa, esperado in (("a", "Bearer token-a"), ("b", "Bearer token-b")):
        c = BlingClient("cid", "cs", empresa=empresa, token_store=store,
                        rate_limiter=limiter, http_client=http)
        c.produtos.listar()
        assert rota.calls[-1].request.headers["authorization"] == esperado


# --- ciclo de vida -------------------------------------------------------------------------


@respx.mock
def test_context_manager_fecha_cliente_proprio(store, limiter):
    with BlingClient("cid", "cs", empresa="t", token_store=store, rate_limiter=limiter) as c:
        http = c._http
    assert http.is_closed


@respx.mock
def test_cliente_http_injetado_nao_e_fechado(store, limiter):
    externo = httpx.Client()
    with BlingClient("cid", "cs", empresa="t", token_store=store, rate_limiter=limiter,
                     http_client=externo):
        pass
    assert not externo.is_closed
    externo.close()


# --- rate limiter --------------------------------------------------------------------------


@respx.mock
def test_limiter_e_chamado_em_toda_requisicao(cliente, limiter):
    respx.get(f"{HOST}/produtos").respond(json={"data": []})
    cliente.produtos.listar()
    cliente.produtos.listar()
    assert limiter.acquires == 2
