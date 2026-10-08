from datetime import date, datetime
from decimal import Decimal
from enum import Enum

import httpx
import pytest

from bling_sdk._core import Core, normalizar_params, validar_intervalo_datas
from bling_sdk.config import CABECALHO_JWT
from bling_sdk.errors import (
    BlingErroServidor,
    BlingErroTransporte,
    BlingErroValidacao,
    BlingIntervaloInvalido,
)
from bling_sdk.models import BlingModel


class Situacao(str, Enum):
    ATIVO = "A"


class Produtinho(BlingModel):
    id: int | None = None
    nome: str | None = None


def resp(status=200, json=None, text=None, headers=None):
    kw = {"headers": headers or {}}
    if json is not None:
        kw["json"] = json
    elif text is not None:
        kw["text"] = text
    return httpx.Response(status, request=httpx.Request("GET", "https://x/y"), **kw)


# --- desembrulho de `data` ---------------------------------------------------------------


def test_desembrulha_objeto():
    assert Core().parse(resp(json={"data": {"id": 1}})) == {"id": 1}


def test_desembrulha_array():
    assert Core().parse(resp(json={"data": [{"id": 1}, {"id": 2}]})) == [{"id": 1}, {"id": 2}]


def test_payload_sem_data_passa_direto():
    assert Core().parse(resp(json={"id": 1})) == {"id": 1}


def test_204_vira_none():
    assert Core().parse(resp(204)) is None


def test_corpo_vazio_vira_none():
    assert Core().parse(resp(200, text="")) is None


def test_modelo_valida_o_data_desembrulhado():
    p = Core().parse(resp(json={"data": {"id": 7, "nome": "Copo"}}), modelo=Produtinho)
    assert (p.id, p.nome) == (7, "Copo")


def test_lista_de_valida_cada_item():
    itens = Core().parse(resp(json={"data": [{"id": 1}, {"id": 2}]}), lista_de=Produtinho)
    assert [i.id for i in itens] == [1, 2]


def test_bruto_devolve_a_resposta():
    r = resp(json={"data": 1})
    assert Core().parse(r, bruto=True) is r


def test_corpo_nao_json_vira_erro_de_transporte():
    with pytest.raises(BlingErroTransporte, match="nao-JSON"):
        Core().parse(resp(200, text="<html>nope</html>"), metodo="GET", path="/produtos")


def test_4xx_sem_json_ainda_vira_erro_de_api():
    # Um bloqueio de IP vem do edge/WAF, nao da API, e nao traz o envelope JSON.
    with pytest.raises(BlingErroValidacao):
        Core().parse(resp(400, text="<html>blocked</html>"))


def test_5xx_sem_corpo_vira_erro_de_servidor():
    with pytest.raises(BlingErroServidor):
        Core().parse(resp(503, text=""))


def test_erro_no_envelope_com_status_200():
    with pytest.raises(BlingErroValidacao):
        Core().parse(resp(200, json={"error": {"type": "VALIDATION_ERROR", "message": "m"}}))


# --- normalizacao de params --------------------------------------------------------------


def test_none_e_descartado():
    assert normalizar_params({"a": 1, "b": None}) == {"a": 1}


def test_params_vazio_vira_none():
    assert normalizar_params({}) is None
    assert normalizar_params({"a": None}) is None


def test_bool_vira_string():
    assert normalizar_params({"a": True, "b": False}) == {"a": "true", "b": "false"}


def test_data_e_datahora():
    out = normalizar_params({"d": date(2024, 9, 27), "dh": datetime(2024, 9, 27, 11, 24, 56)})
    assert out == {"d": "2024-09-27", "dh": "2024-09-27 11:24:56"}


def test_enum_e_decimal():
    assert normalizar_params({"s": Situacao.ATIVO, "p": Decimal("9.90")}) == {"s": "A", "p": "9.90"}


def test_lista_ganha_sufixo_de_array():
    assert normalizar_params({"idsProdutos": [1, 2]}) == {"idsProdutos[]": [1, 2]}


def test_sufixo_nao_e_duplicado():
    assert normalizar_params({"gtins[]": ["x"]}) == {"gtins[]": ["x"]}


def test_lista_vazia_e_descartada():
    assert normalizar_params({"ids": []}) is None


# --- guarda de um ano --------------------------------------------------------------------


def test_intervalo_acima_de_um_ano_levanta_sem_http():
    with pytest.raises(BlingIntervaloInvalido, match="um ano"):
        validar_intervalo_datas({"dataInicial": "2023-01-01", "dataFinal": "2024-06-01"})


def test_366_dias_passa():
    validar_intervalo_datas({"dataInicial": date(2024, 1, 1), "dataFinal": date(2025, 1, 1)})


def test_guarda_vale_para_qualquer_prefixo():
    with pytest.raises(BlingIntervaloInvalido):
        validar_intervalo_datas(
            {"dataAlteracaoInicial": "2020-01-01", "dataAlteracaoFinal": "2026-01-01"}
        )


def test_inicial_sem_final_e_ignorado():
    validar_intervalo_datas({"dataInicial": "2000-01-01"})


def test_guarda_roda_no_prepare():
    with pytest.raises(BlingIntervaloInvalido):
        Core().prepare("GET", "produtos", params={"dataInicial": "2000-01-01", "dataFinal": "2026-01-01"})


# --- prepare -----------------------------------------------------------------------------


def test_header_jwt_presente_por_padrao():
    p = Core().prepare("GET", "produtos", access_token="tok")
    assert p.headers[CABECALHO_JWT] == "1"
    assert p.headers["Authorization"] == "Bearer tok"


def test_header_jwt_ausente_quando_desligado():
    assert CABECALHO_JWT not in Core(enable_jwt=False).prepare("GET", "produtos").headers


def test_content_type_so_com_corpo():
    assert "Content-Type" not in Core().prepare("GET", "produtos").headers
    assert Core().prepare("POST", "produtos", json={}).headers["Content-Type"] == "application/json"


def test_url_monta_com_e_sem_barra():
    c = Core(base_url="https://api.bling.com.br/Api/v3")
    assert c.prepare("GET", "produtos").url == "https://api.bling.com.br/Api/v3/produtos"
    assert c.prepare("GET", "/produtos").url == "https://api.bling.com.br/Api/v3/produtos"


def test_post_e_nao_idempotente_por_padrao():
    assert Core().prepare("POST", "estoques", json={}).idempotente is False
    assert Core().prepare("GET", "produtos").idempotente is True
    assert Core().prepare("PATCH", "produtos/1", json={}).idempotente is True


def test_idempotente_pode_ser_forcado():
    assert Core().prepare("POST", "x", idempotente=True).idempotente is True
    assert Core().prepare("PUT", "x", idempotente=False).idempotente is False


def test_metodo_e_normalizado_para_maiusculo():
    assert Core().prepare("get", "produtos").method == "GET"
