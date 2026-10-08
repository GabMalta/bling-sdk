"""OAuth 2.0 request builders -- sans-IO.

Bling uses only the authorization_code grant. The flow:

1. send the user to :func:`url_autorizacao`;
2. Bling redirects back to the app's registered URL with ``?code=`` (valid for 60 seconds);
3. exchange it at ``POST /oauth/token`` with Basic auth;
4. refresh with ``grant_type=refresh_token`` before the 6-hour access token expires.
"""

from __future__ import annotations

import base64
import secrets
from urllib.parse import urlencode

from ..config import CABECALHO_JWT, OAUTH_AUTHORIZE_URL


def gerar_state(n: int = 32) -> str:
    """A unique, unguessable value echoed back by Bling, to defeat CSRF."""
    return secrets.token_urlsafe(n)


def url_autorizacao(
    client_id: str,
    state: str,
    *,
    base: str = OAUTH_AUTHORIZE_URL,
) -> str:
    """The URL the account owner opens to authorize the app.

    Sends **only** ``response_type``, ``client_id`` and ``state``. ``redirect_uri`` and
    ``scope`` are deliberately omitted: the RFC makes them optional and Bling ignores them
    in the request, always using the values registered on the app. That is precisely why a
    403 ``insufficient_scope`` is fixed in the Bling panel and not in this code.
    """
    params = {"response_type": "code", "client_id": client_id, "state": state}
    return f"{base}?{urlencode(params)}"


def cabecalho_basic(client_id: str, client_secret: str) -> str:
    par = f"{client_id}:{client_secret}".encode()
    return "Basic " + base64.b64encode(par).decode()


def cabecalhos_token(client_id: str, client_secret: str, *, enable_jwt: bool = True) -> dict[str, str]:
    """Headers for ``POST /oauth/token`` and ``POST /oauth/revoke``.

    ``Accept: 1.0`` is verbatim from the Bling docs. It looks like a bug -- it is not a
    media type -- but it is what the documented examples send.
    """
    cabecalhos = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "1.0",
        "Authorization": cabecalho_basic(client_id, client_secret),
    }
    if enable_jwt:
        cabecalhos[CABECALHO_JWT] = "1"
    return cabecalhos


def corpo_authorization_code(code: str) -> dict[str, str]:
    return {"grant_type": "authorization_code", "code": code}


def corpo_refresh_token(refresh_token: str) -> dict[str, str]:
    return {"grant_type": "refresh_token", "refresh_token": refresh_token}


def corpo_revoke(
    token: str,
    token_type_hint: str = "refresh_token",
    *,
    revoke_action: str | None = None,
    revoke_target: str | None = None,
) -> dict[str, str]:
    """Body for ``POST /oauth/revoke``.

    ``revoke_action`` (``logout`` | ``uninstall``) and ``revoke_target`` (``user`` |
    ``company``) widen the blast radius well beyond the token passed in, and the effect is
    irreversible. Omitted by default, so only the given token is revoked.
    """
    corpo = {"token": token, "token_type_hint": token_type_hint}
    if revoke_action:
        corpo["revoke_action"] = revoke_action
    if revoke_target:
        corpo["revoke_target"] = revoke_target
    return corpo
