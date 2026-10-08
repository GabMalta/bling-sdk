"""Politica de retry ponta a ponta.

A regra central: GET/PUT/PATCH/DELETE repetem em 429, 5xx e erro de rede. POST repete **so
em 429** -- um 429 e recusado antes do processamento, mas um 5xx ou timeout em
`POST /estoques` pode significar que o Bling LANCOU o movimento e perdeu so a resposta.
"""

import httpx
import pytest
import respx

from bling_sdk import (
    BlingErroServidor,
    BlingErroTransporte,
    BlingLimiteDiario,
    BlingLimitePorSegundo,
)
from conftest import HOST

ERRO_429_SEGUNDO = {
    "error": {
        "type": "TOO_MANY_REQUESTS",
        "message": "Limite de requisicoes atingido.",
        "description": "O limite de requisicoes por segundo foi atingido.",
        "limit": 3,
        "period": "second",
    }
}
ERRO_429_DIA = {
    "error": {
        "type": "TOO_MANY_REQUESTS",
        "message": "Limite de requisicoes atingido.",
        "description": "O limite de requisicoes por dia foi atingido.",
        "limit": 120000,
        "period": "day",
    }
}
ERRO_500 = {"error": {"type": "SERVER_ERROR", "message": "m", "description": "d"}}


# --- GET: idempotente, repete de tudo ------------------------------------------------------


@respx.mock
def test_get_repete_500_e_sucede(cliente, esperas):
    rota = respx.get(f"{HOST}/produtos").mock(
        side_effect=[
            httpx.Response(500, json=ERRO_500),
            httpx.Response(200, json={"data": [{"id": 1}]}),
        ]
    )
    assert [p.id for p in cliente.produtos.listar()] == [1]
    assert rota.call_count == 2
    assert esperas == [2.0]


@respx.mock
def test_get_repete_erro_de_rede(cliente):
    rota = respx.get(f"{HOST}/produtos").mock(
        side_effect=[httpx.ConnectError("boom"), httpx.Response(200, json={"data": []})]
    )
    cliente.produtos.listar()
    assert rota.call_count == 2


@respx.mock
def test_get_desiste_depois_de_max_tentativas(cliente):
    rota = respx.get(f"{HOST}/produtos").respond(500, json=ERRO_500)
    with pytest.raises(BlingErroServidor):
        cliente.produtos.listar()
    assert rota.call_count == 4  # max_tentativas


@respx.mock
def test_erro_de_rede_persistente_vira_erro_de_transporte(cliente):
    respx.get(f"{HOST}/produtos").mock(side_effect=httpx.ConnectTimeout("timeout"))
    with pytest.raises(BlingErroTransporte, match="4 tentativas"):
        cliente.produtos.listar()


@respx.mock
def test_backoff_exponencial_acumula(cliente, esperas):
    respx.get(f"{HOST}/produtos").respond(500, json=ERRO_500)
    with pytest.raises(BlingErroServidor):
        cliente.produtos.listar()
    assert esperas == [2.0, 4.0, 8.0]


@respx.mock
def test_retry_after_e_honrado(cliente, esperas):
    respx.get(f"{HOST}/produtos").mock(
        side_effect=[
            httpx.Response(503, json=ERRO_500, headers={"Retry-After": "7"}),
            httpx.Response(200, json={"data": []}),
        ]
    )
    cliente.produtos.listar()
    assert esperas == [7.0]


# --- POST: nao idempotente ----------------------------------------------------------------


@respx.mock
def test_post_nao_repete_500(cliente, esperas):
    """Um 5xx no POST /estoques pode ter lancado o movimento e perdido so a resposta."""
    rota = respx.post(f"{HOST}/estoques").respond(500, json=ERRO_500)
    with pytest.raises(BlingErroServidor):
        cliente.estoques.lancar(1, operacao="E", quantidade=5)
    assert rota.call_count == 1, "retry num POST de estoque duplicaria o movimento"
    assert esperas == []


@respx.mock
def test_post_nao_repete_erro_de_rede(cliente):
    rota = respx.post(f"{HOST}/estoques").mock(side_effect=httpx.ConnectTimeout("t"))
    with pytest.raises(BlingErroTransporte, match="rede"):
        cliente.estoques.lancar(1, operacao="S", quantidade=2)
    assert rota.call_count == 1


@respx.mock
def test_post_repete_429(cliente, limiter):
    """Um 429 foi recusado antes do processamento, entao repetir e seguro."""
    rota = respx.post(f"{HOST}/estoques").mock(
        side_effect=[
            httpx.Response(429, json=ERRO_429_SEGUNDO),
            httpx.Response(200, json={"data": {"id": 5}}),
        ]
    )
    cliente.estoques.lancar(1, operacao="E", quantidade=1)
    assert rota.call_count == 2
    assert limiter.penalidades == [2.0]


@respx.mock
def test_acao_de_pedido_tambem_nao_repete_500(cliente):
    """lancar-estoque parece uma acao repetivel. Nao e."""
    rota = respx.post(f"{HOST}/pedidos/vendas/9/lancar-estoque").respond(500, json=ERRO_500)
    with pytest.raises(BlingErroServidor):
        cliente.pedidos.vendas.lancar_estoque(9)
    assert rota.call_count == 1


@respx.mock
def test_idempotente_true_libera_retry_em_post(cliente):
    rota = respx.post(f"{HOST}/coisa").mock(
        side_effect=[httpx.Response(500, json=ERRO_500), httpx.Response(200, json={"data": 1})]
    )
    assert cliente.request("POST", "coisa", json={}, idempotente=True) == 1
    assert rota.call_count == 2


@respx.mock
def test_idempotente_false_bloqueia_retry_em_get(cliente):
    rota = respx.get(f"{HOST}/coisa").respond(500, json=ERRO_500)
    with pytest.raises(BlingErroServidor):
        cliente.request("GET", "coisa", idempotente=False)
    assert rota.call_count == 1


# --- 429 -----------------------------------------------------------------------------------


@respx.mock
def test_429_por_segundo_penaliza_o_limiter_sem_dormir(cliente, limiter, esperas):
    """A pausa vive no limiter, que bloqueia TODAS as threads no proximo acquire()."""
    respx.get(f"{HOST}/produtos").mock(
        side_effect=[
            httpx.Response(429, json=ERRO_429_SEGUNDO),
            httpx.Response(200, json={"data": []}),
        ]
    )
    cliente.produtos.listar()
    assert limiter.penalidades == [2.0]
    assert esperas == [], "no 429 a espera e do limiter, nao um sleep local"


@respx.mock
def test_429_diario_falha_rapido(cliente, limiter):
    rota = respx.get(f"{HOST}/produtos").respond(429, json=ERRO_429_DIA)
    with pytest.raises(BlingLimiteDiario) as info:
        cliente.produtos.listar()
    assert rota.call_count == 1, "esperar nao ajuda: a cota do dia acabou"
    assert limiter.penalidades == [], "nao faz sentido pausar threads por horas"
    assert (info.value.limite, info.value.periodo) == (120000, "day")


@respx.mock
def test_429_persistente_levanta_limite_por_segundo(cliente):
    respx.get(f"{HOST}/produtos").respond(429, json=ERRO_429_SEGUNDO)
    with pytest.raises(BlingLimitePorSegundo):
        cliente.produtos.listar()


@respx.mock
def test_429_honra_retry_after(cliente, limiter):
    respx.get(f"{HOST}/produtos").mock(
        side_effect=[
            httpx.Response(429, json=ERRO_429_SEGUNDO, headers={"Retry-After": "11"}),
            httpx.Response(200, json={"data": []}),
        ]
    )
    cliente.produtos.listar()
    assert limiter.penalidades == [11.0]


@respx.mock
def test_limiter_e_chamado_em_cada_tentativa(cliente, limiter):
    respx.get(f"{HOST}/produtos").mock(
        side_effect=[
            httpx.Response(500, json=ERRO_500),
            httpx.Response(500, json=ERRO_500),
            httpx.Response(200, json={"data": []}),
        ]
    )
    cliente.produtos.listar()
    assert limiter.acquires == 3, "o retry tem de consumir slot, senao amplifica o estouro"
