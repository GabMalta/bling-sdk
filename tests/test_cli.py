"""O fluxo do `bling auth` ponta a ponta, com o Bling mockado e o navegador desligado."""

import threading
import urllib.request
from urllib.parse import parse_qs, urlparse

import pytest
import respx

from bling_sdk.auth.cli import main
from bling_sdk.auth.stores import JSONFileTokenStore
from conftest import OAUTH_REVOKE, OAUTH_TOKEN, token

RESPOSTA_TOKEN = {
    "access_token": "access-do-cli",
    "expires_in": 21600,
    "token_type": "Bearer",
    "scope": "1 2 3",
    "refresh_token": "refresh-do-cli",
}


@pytest.fixture
def tokens(tmp_path):
    return tmp_path / "tokens.json"


def _responder_callback(porta, state_box, *, erro=None, state_errado=False):
    """Espera o servidor subir, le o state da URL impressa e bate no callback."""

    def trabalhar():
        state = state_box.get(timeout=10)
        qs = f"state={'errado' if state_errado else state}"
        qs += f"&error={erro}" if erro else "&code=codigo-valido"
        for _ in range(100):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{porta}/callback?{qs}", timeout=5).read()
                return
            except OSError:
                threading.Event().wait(0.05)

    t = threading.Thread(target=trabalhar, daemon=True)
    t.start()
    return t


class _Caixa:
    """Passa o state do stdout do CLI para a thread do callback."""

    def __init__(self):
        self._evento = threading.Event()
        self._valor = None

    def set(self, valor):
        self._valor = valor
        self._evento.set()

    def get(self, timeout):
        self._evento.wait(timeout)
        return self._valor


def _rodar_auth(capsys, tokens, porta, caixa, **kw):
    thread = _responder_callback(porta, caixa, **kw)

    # O state so e conhecido depois que o CLI imprime a URL, entao espionamos o print.
    import builtins

    original = builtins.print

    def espiao(*args, **kwargs):
        original(*args, **kwargs)
        texto = " ".join(str(a) for a in args)
        if "oauth/authorize" in texto:
            url = texto.strip().split()[-1]
            caixa.set(parse_qs(urlparse(url).query)["state"][0])

    builtins.print = espiao
    try:
        codigo = main(
            [
                "auth",
                "--empresa",
                "teste",
                "--tokens",
                str(tokens),
                "--client-id",
                "cid",
                "--client-secret",
                "csec",
                "--porta",
                str(porta),
                "--no-browser",
                "--timeout",
                "15",
            ]
        )
    finally:
        builtins.print = original
    thread.join(timeout=5)
    return codigo


@respx.mock
def test_auth_completa_o_fluxo_e_grava_tokens(capsys, tokens):
    rota = respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    caixa = _Caixa()

    assert _rodar_auth(capsys, tokens, 8731, caixa) == 0

    # O code foi trocado imediatamente -- ele expira em 60s.
    assert parse_qs(rota.calls[0].request.content.decode())["code"] == ["codigo-valido"]

    guardado = JSONFileTokenStore(tokens).get("teste")
    assert guardado.access_token == "access-do-cli"
    assert guardado.refresh_token == "refresh-do-cli"
    assert guardado.jwt is True

    saida = capsys.readouterr().out
    assert "Tokens gravados" in saida
    assert "access-do-cli" not in saida, "o CLI nunca imprime o token"


@respx.mock
def test_auth_rejeita_state_divergente(capsys, tokens):
    rota = respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    assert _rodar_auth(capsys, tokens, 8732, _Caixa(), state_errado=True) == 1
    assert rota.call_count == 0, "nunca trocar o code quando o state nao bate"
    assert not tokens.exists()


@respx.mock
def test_auth_trata_negacao_do_usuario(capsys, tokens):
    rota = respx.post(OAUTH_TOKEN).respond(json=RESPOSTA_TOKEN)
    assert _rodar_auth(capsys, tokens, 8733, _Caixa(), erro="access_denied") == 1
    assert rota.call_count == 0


@respx.mock
def test_auth_sai_com_2_quando_a_troca_falha(capsys, tokens):
    respx.post(OAUTH_TOKEN).respond(
        400, json={"error": {"type": "VALIDATION_ERROR", "message": "code expirado"}}
    )
    assert _rodar_auth(capsys, tokens, 8734, _Caixa()) == 2
    assert not tokens.exists()


def test_auth_sai_com_3_no_timeout(tokens):
    codigo = main(
        [
            "auth", "--empresa", "t", "--tokens", str(tokens),
            "--client-id", "c", "--client-secret", "s",
            "--porta", "8735", "--no-browser", "--timeout", "0.3",
        ]
    )
    assert codigo == 3


def test_auth_sem_credenciais_orienta(monkeypatch, tokens):
    monkeypatch.delenv("BLING_CLIENT_ID", raising=False)
    monkeypatch.delenv("BLING_CLIENT_SECRET", raising=False)
    with pytest.raises(SystemExit, match="BLING_CLIENT_ID"):
        main(["auth", "--tokens", str(tokens)])


def test_credenciais_vem_do_ambiente(monkeypatch, tokens):
    monkeypatch.setenv("BLING_CLIENT_ID", "do-env")
    monkeypatch.setenv("BLING_CLIENT_SECRET", "secreto")
    assert main(["auth", "--tokens", str(tokens), "--porta", "8736",
                 "--no-browser", "--timeout", "0.3"]) == 3


# --- info ------------------------------------------------------------------------------------


def test_info_mostra_validade_sem_vazar_o_token(capsys, tokens):
    JSONFileTokenStore(tokens).set("teste", token("segredo-absoluto", "r"))
    assert main(["info", "--tokens", str(tokens)]) == 0
    saida = capsys.readouterr().out
    assert "teste:" in saida
    assert "expira em" in saida
    assert "segredo-absoluto" not in saida


def test_info_sem_tokens_orienta(capsys, tokens):
    assert main(["info", "--tokens", str(tokens)]) == 1
    assert "bling auth" in capsys.readouterr().err


def test_info_de_uma_empresa(capsys, tokens):
    store = JSONFileTokenStore(tokens)
    store.set("a", token())
    store.set("b", token())
    main(["info", "--tokens", str(tokens), "--empresa", "a"])
    saida = capsys.readouterr().out
    assert "a:" in saida and "b:" not in saida


# --- revoke / empresa ------------------------------------------------------------------------


@respx.mock
def test_revoke(capsys, tokens):
    JSONFileTokenStore(tokens).set("t", token("a", "refresh-a-revogar"))
    rota = respx.post(OAUTH_REVOKE).respond(200, json={})
    codigo = main(["revoke", "--empresa", "t", "--tokens", str(tokens),
                   "--client-id", "c", "--client-secret", "s"])
    assert codigo == 0
    corpo = parse_qs(rota.calls[0].request.content.decode())
    assert corpo["token"] == ["refresh-a-revogar"]
    assert "revoke_action" not in corpo, "revogacao ampliada so quando pedida"


@respx.mock
def test_empresa_imprime_dados_basicos(capsys, tokens):
    JSONFileTokenStore(tokens).set("t", token())
    respx.get("https://api.bling.com.br/Api/v3/empresas/me/dados-basicos").respond(
        json={"data": {"id": 1, "nome": "Minha Empresa"}}
    )
    assert main(["empresa", "--empresa", "t", "--tokens", str(tokens),
                 "--client-id", "c", "--client-secret", "s"]) == 0
    assert "Minha Empresa" in capsys.readouterr().out
