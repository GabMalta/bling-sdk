import threading
import time
from urllib.parse import parse_qs, urlparse

import httpx
import pytest
import respx

from bling_sdk import BlingClient, BlingSemToken, InMemoryTokenStore, Token
from bling_sdk.auth import cabecalho_basic, url_autorizacao
from bling_sdk.config import CABECALHO_JWT
from conftest import HOST, OAUTH_REVOKE, OAUTH_TOKEN, LimiterEspiao, token

RESPOSTA_TOKEN = {
    "access_token": "novo-access",
    "expires_in": 21600,
    "token_type": "Bearer",
    "scope": "98309 318257570 5862218180",
    "refresh_token": "novo-refresh",
}


# --- URL de autorizacao --------------------------------------------------------------------


def test_url_autorizacao_nao_envia_redirect_uri_nem_scope():
    """O Bling IGNORA os dois na request e usa sempre o que esta cadastrado no app.

    E por isso que um 403 insufficient_scope se conserta no painel, nao no codigo.
    """
    q = parse_qs(urlparse(url_autorizacao("meu-id", "meu-state")).query)
    assert q == {"response_type": ["code"], "client_id": ["meu-id"], "state": ["meu-state"]}


def test_url_autorizacao_usa_o_host_www():
    url = url_autorizacao("id", "s")
    assert url.startswith("https://www.bling.com.br/Api/v3/oauth/authorize?")


def test_cliente_gera_state_quando_nao_informado(cliente):
    url, state = cliente.url_autorizacao()
    assert len(state) > 20
    assert f"state={state}" in url


def test_cabecalho_basic():
    assert cabecalho_basic("abc", "123") == "Basic YWJjOjEyMw=="


# --- troca do authorization code -----------------------------------------------------------


@respx.mock
def test_troca_codigo_envia_basic_urlencoded_e_jwt(cliente, store):
    rota = respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    t = cliente.trocar_codigo("codigo-de-um-minuto")

    req = rota.calls[0].request
    assert req.headers["authorization"] == cabecalho_basic("cid", "csecret")
    assert req.headers["content-type"] == "application/x-www-form-urlencoded"
    assert req.headers["accept"] == "1.0"  # literal, verbatim da doc do Bling
    assert req.headers[CABECALHO_JWT] == "1"
    assert parse_qs(req.content.decode()) == {
        "grant_type": ["authorization_code"],
        "code": ["codigo-de-um-minuto"],
    }

    assert t.access_token == "novo-access"
    assert t.jwt is True
    assert t.escopos() == ["98309", "318257570", "5862218180"]
    assert store.get("t").access_token == "novo-access"


@respx.mock
def test_expires_at_vem_de_expires_in(cliente):
    respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    antes = time.time()
    t = cliente.trocar_codigo("c")
    assert antes + 21600 <= t.expires_at <= time.time() + 21600


@respx.mock
def test_sem_jwt_o_header_nao_vai(store, limiter, http):
    c = BlingClient("cid", "csecret", empresa="t", token_store=store, rate_limiter=limiter,
                    enable_jwt=False, http_client=http)
    rota = respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    assert c.trocar_codigo("c").jwt is False
    assert CABECALHO_JWT not in rota.calls[0].request.headers


# --- renovacao -----------------------------------------------------------------------------


@respx.mock
def test_token_valido_nao_dispara_renovacao(cliente):
    rota_token = respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    respx.get(f"{HOST}/produtos").respond(json={"data": []})
    cliente.produtos.listar()
    assert rota_token.call_count == 0


@respx.mock
def test_token_perto_de_expirar_e_renovado_uma_vez(store, limiter, http):
    # 100s restantes, dentro da folga padrao de 300s.
    store.set("t", token("velho", "refresh-velho", expira_em=100))
    c = BlingClient("cid", "cs", empresa="t", token_store=store, rate_limiter=limiter,
                    http_client=http)
    rota_token = respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    rota_api = respx.get(f"{HOST}/produtos").respond(json={"data": []})

    c.produtos.listar()

    assert rota_token.call_count == 1
    assert rota_api.calls[0].request.headers["authorization"] == "Bearer novo-access"
    # O refresh_token ROTA a cada uso: o novo tem de ser persistido ou a autorizacao morre.
    assert store.get("t").refresh_token == "novo-refresh"


@respx.mock
def test_resposta_sem_refresh_token_preserva_o_anterior(store, limiter, http):
    store.set("t", token("velho", "refresh-que-funciona", expira_em=10))
    c = BlingClient("cid", "cs", empresa="t", token_store=store, rate_limiter=limiter,
                    http_client=http)
    respx.post(OAUTH_TOKEN).respond(json={"access_token": "a", "expires_in": 21600})
    respx.get(f"{HOST}/produtos").respond(json={"data": []})
    c.produtos.listar()
    assert store.get("t").refresh_token == "refresh-que-funciona"


@respx.mock
def test_oito_threads_causam_uma_unica_chamada_de_token(store, limiter, http):
    """Bling bane o IP por 60 min com 20 chamadas a /oauth/token em 60s."""
    store.set("t", token("velho", "r", expira_em=10))
    c = BlingClient("cid", "cs", empresa="t", token_store=store, rate_limiter=limiter,
                    http_client=http)
    rota_token = respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    respx.get(f"{HOST}/produtos").respond(json={"data": []})

    erros: list[BaseException] = []

    def trabalhar():
        try:
            c.produtos.listar()
        except BaseException as exc:  # noqa: BLE001
            erros.append(exc)

    threads = [threading.Thread(target=trabalhar) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert erros == []
    assert rota_token.call_count == 1


@respx.mock
def test_401_forca_uma_renovacao_e_um_retry(cliente, store):
    """Um token pode ser revogado no servidor antes do expires_at."""
    rota_token = respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    rota_api = respx.get(f"{HOST}/produtos").mock(
        side_effect=[
            httpx.Response(401, json={"error": {"type": "invalid_token", "message": "m"}}),
            httpx.Response(200, json={"data": [{"id": 1}]}),
        ]
    )
    assert [p.id for p in cliente.produtos.listar()] == [1]
    assert rota_token.call_count == 1
    assert rota_api.call_count == 2
    assert rota_api.calls[1].request.headers["authorization"] == "Bearer novo-access"


@respx.mock
def test_401_persistente_nao_renova_em_loop(cliente):
    rota_token = respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    rota_api = respx.get(f"{HOST}/produtos").respond(
        401, json={"error": {"type": "invalid_token", "message": "m"}}
    )
    with pytest.raises(Exception):  # noqa: B017 - BlingNaoAutenticado
        cliente.produtos.listar()
    assert rota_token.call_count == 1, "uma renovacao forcada, nao um loop"
    assert rota_api.call_count == 2


@respx.mock
def test_renovar_token_explicito(cliente, store):
    respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    assert cliente.renovar_token().access_token == "novo-access"


@respx.mock
def test_renovacao_usa_limiter_proprio_para_o_endpoint_de_token(store, limiter, http):
    store.set("t", token("velho", "r", expira_em=10))
    limiter_token = LimiterEspiao()
    c = BlingClient("cid", "cs", empresa="t", token_store=store, rate_limiter=limiter,
                    http_client=http)
    c._limiter_token = limiter_token
    respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    respx.get(f"{HOST}/produtos").respond(json={"data": []})
    c.produtos.listar()
    assert limiter_token.acquires == 1


@respx.mock
def test_sem_refresh_token_levanta(limiter, http):
    store = InMemoryTokenStore()
    store.set("t", Token(access_token="a", refresh_token="", expires_at=0))
    c = BlingClient("cid", "cs", empresa="t", token_store=store, rate_limiter=limiter,
                    http_client=http)
    with pytest.raises(BlingSemToken, match="refresh_token"):
        c.produtos.listar()


# --- revoke --------------------------------------------------------------------------------


@respx.mock
def test_revogar_envia_token_type_hint(cliente):
    rota = respx.post(OAUTH_REVOKE).respond(200, json={})
    cliente.revogar()
    corpo = parse_qs(rota.calls[0].request.content.decode())
    assert corpo == {"token": ["ref"], "token_type_hint": ["refresh_token"]}


@respx.mock
def test_revogar_avancado_so_quando_pedido(cliente):
    rota = respx.post(OAUTH_REVOKE).respond(200, json={})
    cliente.revogar(acao="uninstall", alvo="company")
    corpo = parse_qs(rota.calls[0].request.content.decode())
    assert corpo["revoke_action"] == ["uninstall"]
    assert corpo["revoke_target"] == ["company"]


@respx.mock
def test_revogar_aceita_resposta_vazia(cliente):
    respx.post(OAUTH_REVOKE).respond(200, content=b"")
    cliente.revogar()  # nao deve levantar


@respx.mock
def test_revogar_sem_token_levanta(cliente_sem_token):
    with pytest.raises(BlingSemToken):
        cliente_sem_token.revogar()


# --- seguranca do Token --------------------------------------------------------------------


def test_repr_do_token_nao_vaza():
    t = token("segredo-do-access", "segredo-do-refresh")
    assert "segredo" not in repr(t)
    assert "segredo" not in str(t)
    assert "***" in repr(t)


@respx.mock
def test_jwt_longo_chega_intacto_ao_header(store, limiter, http):
    jwt_longo = "eyJ" + "a" * 2900
    store.set("t", Token(access_token=jwt_longo, refresh_token="r",
                         expires_at=time.time() + 3600, jwt=True))
    c = BlingClient("cid", "cs", empresa="t", token_store=store, rate_limiter=limiter,
                   http_client=http)
    rota = respx.get(f"{HOST}/produtos").respond(json={"data": []})
    c.produtos.listar()
    assert rota.calls[0].request.headers["authorization"] == f"Bearer {jwt_longo}"


@respx.mock
def test_token_opaco_sob_jwt_gera_aviso_uma_vez(store, limiter, http, caplog):
    store.set("t", token("opaco", jwt=False))
    c = BlingClient("cid", "cs", empresa="t", token_store=store, rate_limiter=limiter,
                    http_client=http)
    respx.get(f"{HOST}/produtos").respond(json={"data": []})
    with caplog.at_level("WARNING", logger="bling_sdk"):
        c.produtos.listar()
        c.produtos.listar()
    avisos = [r for r in caplog.records if "token opaco" in r.message]
    assert len(avisos) == 1
