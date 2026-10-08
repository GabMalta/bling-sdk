import time

import pytest

from bling_sdk import BlingClient, InMemoryTokenStore, SemLimite, Token
from bling_sdk.config import API_BASE
from bling_sdk.ratelimit import limpar_limitadores

HOST = API_BASE
OAUTH_TOKEN = "https://api.bling.com.br/Api/v3/oauth/token"
OAUTH_REVOKE = "https://api.bling.com.br/Api/v3/oauth/revoke"


def token(access="tok", refresh="ref", expira_em=3600, jwt=True):
    return Token(
        access_token=access,
        refresh_token=refresh,
        expires_at=time.time() + expira_em,
        jwt=jwt,
    )


class LimiterEspiao:
    """Records calls without ever sleeping, so retry tests stay fast."""

    def __init__(self):
        self.acquires = 0
        self.penalidades: list[float] = []

    def acquire(self):
        self.acquires += 1

    def penalize(self, segundos):
        self.penalidades.append(segundos)


@pytest.fixture(autouse=True)
def _sem_limitadores_globais():
    """Keep the per-company limiter registry from leaking between tests."""
    limpar_limitadores()
    yield
    limpar_limitadores()


class _TempoFalso:
    """Stand-in for the ``time`` module as seen by ``bling_sdk.client``.

    Swapping the *name* ``bling_sdk.client.time`` rather than ``time.sleep`` matters:
    ``bling_sdk.client.time`` IS the global time module, so patching its ``sleep`` attribute
    would patch sleeping for the whole process -- and silently break the rate-limiter tests,
    whose entire job is to measure real elapsed time.
    """

    def __init__(self, esperas: list[float]) -> None:
        self.esperas = esperas

    def sleep(self, segundos: float) -> None:
        self.esperas.append(segundos)

    def __getattr__(self, nome: str):
        return getattr(time, nome)


@pytest.fixture(autouse=True)
def _sem_dormir(monkeypatch):
    """Nenhum teste deve realmente dormir; registramos as esperas em `esperas`."""
    esperas: list[float] = []
    monkeypatch.setattr("bling_sdk.client.time", _TempoFalso(esperas))
    return esperas


@pytest.fixture
def esperas(_sem_dormir):
    return _sem_dormir


@pytest.fixture(scope="session")
def http():
    """One shared httpx.Client for the whole session.

    Building an httpx.Client loads the system certificate store, which costs most of a
    second on Windows. respx patches the transport, so sharing one is safe -- and tests that
    care about ownership build their own client explicitly.
    """
    import httpx

    with httpx.Client() as cliente_http:
        yield cliente_http


@pytest.fixture
def store():
    s = InMemoryTokenStore()
    s.set("t", token())
    return s


@pytest.fixture
def limiter():
    return LimiterEspiao()


@pytest.fixture
def cliente(store, limiter, http):
    return BlingClient(
        "cid",
        "csecret",
        empresa="t",
        token_store=store,
        rate_limiter=limiter,
        max_tentativas=4,
        http_client=http,
    )


@pytest.fixture
def cliente_sem_token(http):
    return BlingClient(
        "cid",
        "csecret",
        empresa="vazia",
        token_store=InMemoryTokenStore(),
        rate_limiter=SemLimite(),
        http_client=http,
    )
