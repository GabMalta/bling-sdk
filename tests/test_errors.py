"""Os envelopes usados aqui sao copiados literalmente de developer.bling.com.br/erros-comuns."""

import pytest

from bling_sdk.errors import (
    BlingErroAPI,
    BlingErroServidor,
    BlingErroValidacao,
    BlingLimiteDiario,
    BlingLimiteExcedido,
    BlingLimitePorSegundo,
    BlingNaoAutenticado,
    BlingNaoEncontrado,
    BlingSemPermissao,
    error_for,
)

VALIDATION_ERROR = {
    "error": {
        "type": "VALIDATION_ERROR",
        "message": "Nao foi possivel executar a operacao",
        "description": "Ocorreu um erro ao validar os dados recebidos.",
    }
}
MISSING_REQUIRED_FIELD = {
    "error": {
        "type": "MISSING_REQUIRED_FIELD_ERROR",
        "message": "Nao foi possivel executar a operacao",
        "description": "Nenhum dado foi informado na requisicao.",
    }
}
UNKNOWN_ERROR = {
    "error": {
        "type": "UNKNOWN_ERROR",
        "message": "Nao foi possivel executar a operacao",
        "description": "Ocorreu um erro inesperado.",
    }
}
UNAUTHORIZED = {
    "error": {
        "type": "invalid_token",
        "message": "invalid_token",
        "description": "The access token provided is invalid",
    }
}
FORBIDDEN = {
    "error": {
        "type": "insufficient_scope",
        "message": "insufficient_scope",
        "description": "The request requires higher privileges than provided by the access token",
    }
}
NOT_FOUND = {
    "error": {
        "type": "RESOURCE_NOT_FOUND",
        "message": "Recurso nao encontrado",
        "description": "O recurso requisitado nao foi encontrado.",
    }
}
TOO_MANY_SECOND = {
    "error": {
        "type": "TOO_MANY_REQUESTS",
        "message": "Limite de requisicoes atingido.",
        "description": "O limite de requisicoes por segundo foi atingido, tente novamente mais tarde.",
        "limit": 3,
        "period": "second",
    }
}
TOO_MANY_DAY = {
    "error": {
        "type": "TOO_MANY_REQUESTS",
        "message": "Limite de requisicoes atingido.",
        "description": "O limite de requisicoes por dia foi atingido, tente novamente amanha.",
        "limit": 120000,
        "period": "day",
    }
}
SERVER_ERROR = {
    "error": {
        "type": "SERVER_ERROR",
        "message": "Nao foi possivel executar a operacao",
        "description": "Um erro interno ocorreu.",
    }
}


@pytest.mark.parametrize(
    ("status", "payload", "esperado"),
    [
        (400, VALIDATION_ERROR, BlingErroValidacao),
        (400, MISSING_REQUIRED_FIELD, BlingErroValidacao),
        (400, UNKNOWN_ERROR, BlingErroValidacao),
        (401, UNAUTHORIZED, BlingNaoAutenticado),
        (403, FORBIDDEN, BlingSemPermissao),
        (404, NOT_FOUND, BlingNaoEncontrado),
        (429, TOO_MANY_SECOND, BlingLimitePorSegundo),
        (429, TOO_MANY_DAY, BlingLimiteDiario),
        (500, SERVER_ERROR, BlingErroServidor),
    ],
)
def test_cada_envelope_documentado_mapeia(status, payload, esperado):
    assert type(error_for(status, payload, "GET", "/produtos")) is esperado


def test_todo_erro_de_api_herda_de_bling_erro_api():
    assert isinstance(error_for(429, TOO_MANY_DAY), BlingErroAPI)
    assert isinstance(error_for(429, TOO_MANY_DAY), BlingLimiteExcedido)


def test_429_carrega_limit_e_period():
    por_segundo = error_for(429, TOO_MANY_SECOND)
    assert (por_segundo.limite, por_segundo.periodo) == (3, "second")
    diario = error_for(429, TOO_MANY_DAY)
    assert (diario.limite, diario.periodo) == (120000, "day")


def test_mensagem_do_403_e_acionavel():
    msg = str(error_for(403, FORBIDDEN, "GET", "/estoques"))
    assert "painel do Bling" in msg
    assert "bling auth" in msg
    assert "GET /estoques" in msg


def test_payload_cru_sempre_retido():
    e = error_for(400, VALIDATION_ERROR)
    assert e.payload == VALIDATION_ERROR
    assert e.tipo == "VALIDATION_ERROR"
    assert e.descricao.startswith("Ocorreu um erro ao validar")


def test_campos_de_validacao_expostos():
    com_campos = {"error": dict(VALIDATION_ERROR["error"], fields=[{"nome": "preco"}])}
    assert error_for(400, com_campos).campos == [{"nome": "preco"}]
    assert error_for(400, VALIDATION_ERROR).campos is None


def test_tipo_desconhecido_em_status_conhecido_cai_na_classe_certa():
    e = error_for(403, {"error": {"type": "ALGO_NOVO", "message": "m"}})
    assert isinstance(e, BlingSemPermissao)
    assert e.tipo == "ALGO_NOVO"


def test_status_sem_corpo_usa_tipo_padrao():
    assert error_for(404, None).tipo == "RESOURCE_NOT_FOUND"
    assert error_for(401, {}).tipo == "invalid_token"
    assert error_for(503, None).tipo == "SERVER_ERROR"


def test_erro_em_status_2xx_despacha_pelo_tipo():
    assert isinstance(error_for(200, VALIDATION_ERROR), BlingErroValidacao)
    assert isinstance(error_for(200, UNAUTHORIZED), BlingNaoAutenticado)
    assert type(error_for(200, {"error": {"type": "???"}})) is BlingErroAPI


def test_limit_invalido_nao_estoura():
    e = error_for(429, {"error": {"type": "TOO_MANY_REQUESTS", "limit": "muitos"}})
    assert e.limite is None


def test_credencial_na_mensagem_e_redigida():
    e = error_for(400, {"error": {"type": "X", "message": "use Bearer abcdef1234567890"}})
    assert "abcdef1234567890" not in str(e)
    assert "***" in str(e)
