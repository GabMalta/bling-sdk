"""Politica de retry como funcao pura. O comportamento ponta a ponta vive em test_client.py."""

import pytest

from bling_sdk.retry import TETO_BACKOFF, deve_repetir, tempo_espera


def test_retry_after_em_segundos_e_honrado():
    assert tempo_espera(1, "7") == 7.0


def test_retry_after_e_limitado_pelo_teto():
    assert tempo_espera(1, "9999") == TETO_BACKOFF


def test_retry_after_negativo_nao_vira_espera_negativa():
    assert tempo_espera(1, "-5") == 0.0


def test_retry_after_em_http_date_cai_no_backoff():
    assert tempo_espera(3, "Wed, 21 Oct 2015 07:28:00 GMT") == 8.0


def test_backoff_exponencial():
    assert [tempo_espera(t) for t in (1, 2, 3, 4)] == [2.0, 4.0, 8.0, 16.0]


def test_backoff_respeita_o_teto():
    assert tempo_espera(10) == TETO_BACKOFF
    assert tempo_espera(10, teto=5.0) == 5.0


@pytest.mark.parametrize("idempotente", [True, False])
def test_429_por_segundo_sempre_repete(idempotente):
    assert deve_repetir(429, idempotente=idempotente, periodo_429="second") is True


@pytest.mark.parametrize("idempotente", [True, False])
def test_429_diario_nunca_repete(idempotente):
    assert deve_repetir(429, idempotente=idempotente, periodo_429="day") is False


def test_5xx_repete_so_em_verbo_idempotente():
    assert deve_repetir(500, idempotente=True) is True
    assert deve_repetir(503, idempotente=True) is True
    # Um 5xx no POST /estoques pode ter lancado o movimento e perdido so a resposta.
    assert deve_repetir(500, idempotente=False) is False


def test_erro_de_rede_repete_so_em_verbo_idempotente():
    assert deve_repetir(None, idempotente=True) is True
    assert deve_repetir(None, idempotente=False) is False


@pytest.mark.parametrize("status", [200, 201, 400, 401, 403, 404, 422])
def test_nao_repete_sucesso_nem_4xx_de_validacao(status):
    assert deve_repetir(status, idempotente=True) is False
