"""The token model and the storage contract.

Tokens are keyed by ``empresa`` -- a caller-chosen alias for one Bling account -- because
the 3 req/s budget and the token pair are both per-account, and a single process may well
talk to several accounts.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict

from ..config import ACCESS_TOKEN_TTL, FOLGA_RENOVACAO


class Token(BaseModel):
    """One access/refresh pair for one Bling account.

    ``access_token`` is valid for 6 hours and ``refresh_token`` for 30 days. The refresh
    token **rotates on every use**: the response to a refresh carries a new one, and the
    old one stops working. That is why every store write must be atomic and why refreshes
    must be de-duplicated across processes.
    """

    model_config = ConfigDict(extra="allow")

    access_token: str
    refresh_token: str
    #: Unix epoch seconds. Computed from `expires_in` at the moment the token was minted.
    expires_at: float
    token_type: str = "Bearer"
    #: Bling returns space-separated scope *ids*, e.g. "98309 318257570 5862218180".
    scope: str = ""
    #: Whether `enable-jwt: 1` was sent when this token was minted. A stored opaque token
    #: under a JWT-enabled client gets a warning and is upgraded on the next refresh.
    jwt: bool = False
    obtido_em: float = 0.0

    def precisa_renovar(self, folga: float = FOLGA_RENOVACAO) -> bool:
        return time.time() >= self.expires_at - folga

    def expirado(self) -> bool:
        return time.time() >= self.expires_at

    def segundos_restantes(self) -> float:
        return max(0.0, self.expires_at - time.time())

    def escopos(self) -> list[str]:
        return self.scope.split()

    def __repr__(self) -> str:
        """Redacted on purpose.

        A JWT is 1500-3000 characters and is a live credential; it must not land in a
        traceback, a log line or a pytest diff.
        """
        return (
            f"Token(access_token='***', refresh_token='***', "
            f"expires_at={self.expires_at}, jwt={self.jwt})"
        )

    __str__ = __repr__


class TokenStore(Protocol):
    """Persist tokens. Implement this for a DB, a secret manager, anything.

    ``empresa`` is the account alias chosen by the caller.
    """

    def get(self, empresa: str) -> Token | None: ...

    def set(self, empresa: str, token: Token) -> None: ...


@runtime_checkable
class TokenStoreTransacional(Protocol):
    """Optional extra contract for stores that can lock.

    A store implementing this gets cross-process refresh de-duplication for free: the
    client hands it a callback and the store holds its lock across read -> refresh ->
    write. Without it, two processes can refresh concurrently and one of them ends up
    holding a refresh token that Bling has already rotated away.
    """

    def atualizar(self, empresa: str, renovar: Callable[[Token | None], Token]) -> Token: ...


def token_de_payload(
    payload: dict[str, Any],
    *,
    agora: float | None = None,
    jwt: bool = False,
    anterior: Token | None = None,
) -> Token:
    """Build a Token from an ``/oauth/token`` response body.

    Bling always returns a fresh ``refresh_token``, but ``anterior`` is honoured as a
    fallback so a response that omits it cannot wipe a working one.
    """
    instante = time.time() if agora is None else agora
    refresh = payload.get("refresh_token") or (anterior.refresh_token if anterior else "")
    return Token(
        access_token=str(payload["access_token"]),
        refresh_token=str(refresh),
        expires_at=instante + int(payload.get("expires_in", ACCESS_TOKEN_TTL)),
        token_type=str(payload.get("token_type", "Bearer")),
        scope=str(payload.get("scope", "")),
        jwt=jwt,
        obtido_em=instante,
    )
