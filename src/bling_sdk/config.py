"""Hosts, limits and defaults for the Bling v3 API.

Every constant here is sourced from https://developer.bling.com.br. Where a value is a
self-imposed margin rather than a documented limit, the comment says so.
"""

from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

__version__ = "0.1.0"

#: REST base. Note the capital "A" in /Api/v3 -- it is case sensitive.
API_BASE = "https://api.bling.com.br/Api/v3"

#: The authorize endpoint lives on the *www* host (it renders a page for the user),
#: while token/revoke live on the *api* host. Mixing them up yields a 404.
OAUTH_AUTHORIZE_URL = "https://www.bling.com.br/Api/v3/oauth/authorize"
OAUTH_TOKEN_URL = "https://api.bling.com.br/Api/v3/oauth/token"
OAUTH_REVOKE_URL = "https://api.bling.com.br/Api/v3/oauth/revoke"

#: Opaque tokens are deprecated. Sending this header on POST /oauth/token mints a JWT,
#: and it must be kept on every authenticated request for JWT auth to keep working.
CABECALHO_JWT = "enable-jwt"
CABECALHO_ASSINATURA = "X-Bling-Signature-256"
CABECALHO_HOMOLOGACAO = "x-bling-homologacao"

#: Documented default lifetimes. The real values come from the token response; these are
#: only the fallback when `expires_in` is missing.
ACCESS_TOKEN_TTL = 21_600  # 6 h
REFRESH_TOKEN_TTL = 2_592_000  # 30 d

#: Refresh this many seconds before `expires_at`. Generous on purpose: a request that
#: starts valid and lands expired costs a 401 round-trip plus a forced refresh.
FOLGA_RENOVACAO = 300.0

#: Per Bling ACCOUNT, across every endpoint -- not per app, not per token.
REQUISICOES_POR_SEGUNDO = 3
REQUISICOES_POR_DIA = 120_000

#: Bling bans the source IP for 60 minutes at 20 requests to /oauth/token in 60 seconds.
#: We self-impose half of that: a 60-minute ban takes down every company at once, and
#: legitimate load is ~4 refreshes per day per company, so the headroom is free.
TOKEN_REQUESTS_POR_MINUTO = 10

LIMITE_PADRAO = 100

#: GET filters spanning more than a year return HTTP 400. We allow 366 days so the SDK
#: can never refuse something Bling would have accepted.
INTERVALO_MAXIMO_FILTRO = timedelta(days=366)

#: Bling emits and accepts "2024-09-27 11:24:56" -- a space, not the ISO 8601 "T".
FORMATO_DATA = "%Y-%m-%d"
FORMATO_DATA_HORA = "%Y-%m-%d %H:%M:%S"

USER_AGENT = f"bling-sdk/{__version__} (+https://github.com/GabMalta/bling-sdk)"


def diretorio_padrao() -> Path:
    """Where tokens and rate-limit state live. ``BLING_SDK_HOME`` overrides."""
    if env := os.getenv("BLING_SDK_HOME"):
        return Path(env).expanduser()
    return Path.home() / ".config" / "bling-sdk"


def caminho_tokens_padrao() -> Path:
    return diretorio_padrao() / "tokens.json"


def caminho_ratelimit_padrao(empresa: str) -> Path:
    seguro = "".join(c if c.isalnum() or c in "-_" else "_" for c in empresa)
    return diretorio_padrao() / f"ratelimit-{seguro}.json"
