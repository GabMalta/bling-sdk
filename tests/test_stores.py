import json
import sys
import threading
import time

import pytest

from bling_sdk.auth import InMemoryTokenStore, JSONFileTokenStore, Token
from bling_sdk.errors import BlingError


def tok(access="a", refresh="r", expires_at=None):
    return Token(
        access_token=access,
        refresh_token=refresh,
        expires_at=time.time() + 3600 if expires_at is None else expires_at,
    )


@pytest.fixture
def store(tmp_path):
    return JSONFileTokenStore(tmp_path / "tokens.json")


def test_round_trip(store):
    store.set("legitima", tok("abc", "ref"))
    recuperado = store.get("legitima")
    assert (recuperado.access_token, recuperado.refresh_token) == ("abc", "ref")


def test_empresa_desconhecida_devolve_none(store):
    assert store.get("ninguem") is None


def test_empresas_sao_isoladas(store):
    store.set("a", tok("token-a"))
    store.set("b", tok("token-b"))
    assert store.get("a").access_token == "token-a"
    assert store.get("b").access_token == "token-b"
    assert store.listar() == ["a", "b"]


def test_arquivo_tem_versao_e_empresas(store):
    store.set("x", tok())
    dados = json.loads(store.caminho.read_text(encoding="utf-8"))
    assert dados["versao"] == 1
    assert "x" in dados["empresas"]


def test_escrita_nao_deixa_temporario(store):
    store.set("x", tok())
    restos = [p.name for p in store.caminho.parent.iterdir() if ".tmp" in p.name]
    assert restos == []


@pytest.mark.skipif(sys.platform == "win32", reason="NTFS usa ACL; chmod so mexe no read-only")
def test_permissoes_restritas(store):
    store.set("x", tok())
    assert store.caminho.stat().st_mode & 0o777 == 0o600


def test_arquivo_corrompido_levanta_em_vez_de_resetar(store):
    store.caminho.parent.mkdir(parents=True, exist_ok=True)
    store.caminho.write_text("{isso nao e json", encoding="utf-8")
    with pytest.raises(BlingError, match="corrompido"):
        store.get("x")


def test_arquivo_nao_objeto_levanta(store):
    store.caminho.parent.mkdir(parents=True, exist_ok=True)
    store.caminho.write_text("[1, 2, 3]", encoding="utf-8")
    with pytest.raises(BlingError, match="objeto JSON"):
        store.get("x")


def test_remover(store):
    store.set("x", tok())
    assert store.remover("x") is True
    assert store.remover("x") is False
    assert store.get("x") is None


def test_atualizar_recebe_o_token_atual(store):
    store.set("x", tok("velho"))
    visto = []

    def renovar(atual):
        visto.append(atual.access_token if atual else None)
        return tok("novo")

    assert store.atualizar("x", renovar).access_token == "novo"
    assert visto == ["velho"]
    assert store.get("x").access_token == "novo"


def test_atualizar_sem_token_anterior_recebe_none(store):
    store.atualizar("x", lambda atual: tok("primeiro") if atual is None else tok("errado"))
    assert store.get("x").access_token == "primeiro"


def test_atualizar_serializa_threads(store):
    """A trava garante que o callback nao rode concorrente -- Bling rota o refresh_token."""
    store.set("x", tok("v0", "r0"))
    concorrentes = []
    ativo = threading.Lock()

    def renovar(atual):
        adquiriu = ativo.acquire(blocking=False)
        concorrentes.append(adquiriu)
        time.sleep(0.05)
        novo = tok(f"{atual.access_token}+", f"{atual.refresh_token}+")
        if adquiriu:
            ativo.release()
        return novo

    threads = [threading.Thread(target=store.atualizar, args=("x", renovar)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(concorrentes), "dois callbacks rodaram ao mesmo tempo"
    # Cada renovacao viu o resultado da anterior: 4 chamadas encadeadas.
    assert store.get("x").access_token == "v0++++"


def test_token_opcional_jwt_e_escopo_persistem(store):
    store.set("x", Token(access_token="a", refresh_token="r", expires_at=1.0, jwt=True, scope="1 2"))
    recuperado = store.get("x")
    assert recuperado.jwt is True
    assert recuperado.escopos() == ["1", "2"]


# --- InMemory ---------------------------------------------------------------------------


def test_memoria_round_trip_e_atualizar():
    s = InMemoryTokenStore()
    assert s.get("x") is None
    s.set("x", tok("a"))
    assert s.get("x").access_token == "a"
    assert s.atualizar("x", lambda atual: tok(atual.access_token + "!")).access_token == "a!"
