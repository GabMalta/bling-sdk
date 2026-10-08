"""The Bling client -- the only module in this package that performs I/O.

Constructing a client is free and silent: no network call, no token refresh, no filesystem
write, no ``print``, no ``input``. That is enforced by a test, because the integration this
replaces refreshed a token on every construction, printed to stdout, and could block on an
``input()`` prompt.
"""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Mapping
from types import TracebackType
from typing import Any

import httpx
from pydantic import BaseModel

from ._core import Core
from .auth.oauth import (
    cabecalhos_token,
    corpo_authorization_code,
    corpo_refresh_token,
    corpo_revoke,
    gerar_state,
    url_autorizacao,
)
from .auth.stores import JSONFileTokenStore
from .auth.tokens import Token, TokenStore, TokenStoreTransacional, token_de_payload
from .config import (
    API_BASE,
    FOLGA_RENOVACAO,
    OAUTH_REVOKE_URL,
    OAUTH_TOKEN_URL,
    TOKEN_REQUESTS_POR_MINUTO,
)
from .errors import BlingErroTransporte, BlingLimiteDiario, BlingSemToken
from .errors import error_for as _error_for
from .ratelimit import JanelaDeslizanteRateLimiter, RateLimiter, limitador_padrao
from .retry import TETO_BACKOFF, deve_repetir, tempo_espera

logger = logging.getLogger("bling_sdk")


class _Recursos:
    """Attaches the API resource groups to the client."""

    def __init__(self) -> None:
        from .api import (
            CanaisVenda,
            Categorias,
            Contatos,
            Depositos,
            Empresas,
            Estoques,
            Nfe,
            Pedidos,
            Produtos,
            Situacoes,
        )

        self.produtos = Produtos(self)
        self.estoques = Estoques(self)  # type: ignore[arg-type]
        self.depositos = Depositos(self)  # type: ignore[arg-type]
        self.pedidos = Pedidos(self)
        self.contatos = Contatos(self)  # type: ignore[arg-type]
        self.nfe = Nfe(self)  # type: ignore[arg-type]
        self.situacoes = Situacoes(self)
        self.categorias = Categorias(self)
        self.canais_venda = CanaisVenda(self)  # type: ignore[arg-type]
        self.empresas = Empresas(self)  # type: ignore[arg-type]


class BlingClient(_Recursos):
    """Blocking client for the Bling v3 API.

    ``empresa`` is an alias for one Bling account. It keys both the token store and the
    rate limiter, because the 3 req/s budget and the token pair are both per-account. A
    single-account caller never has to type it.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        *,
        empresa: str = "default",
        token_store: TokenStore | None = None,
        rate_limiter: RateLimiter | None = None,
        enable_jwt: bool = True,
        timeout: float = 30.0,
        max_tentativas: int = 4,
        teto_backoff: float = TETO_BACKOFF,
        folga_renovacao: float = FOLGA_RENOVACAO,
        http_client: httpx.Client | None = None,
        base_url: str = API_BASE,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.empresa = empresa
        self.enable_jwt = enable_jwt
        self.max_tentativas = max(1, int(max_tentativas))
        self.teto_backoff = teto_backoff
        self.folga_renovacao = folga_renovacao

        self.core = Core(base_url=base_url, enable_jwt=enable_jwt)
        self.tokens: TokenStore = token_store if token_store is not None else JSONFileTokenStore()
        self._limiter = rate_limiter if rate_limiter is not None else limitador_padrao(empresa)

        # A dedicated limiter for /oauth/token. Bling bans the source IP for 60 minutes at
        # 20 token requests in 60 seconds, and that ban takes down every company at once --
        # so this budget must never be spent by ordinary API traffic.
        self._limiter_token: RateLimiter = JanelaDeslizanteRateLimiter(
            TOKEN_REQUESTS_POR_MINUTO, periodo=60.0
        )

        # `retries=0` is deliberate: a retry inside the transport sits *below* the rate
        # limiter and the per-verb policy, so it consumes no slot and would both amplify a
        # rate-limit overrun and silently re-send a POST.
        self._http_proprio = http_client is None
        self._http = http_client or httpx.Client(
            timeout=timeout, transport=httpx.HTTPTransport(retries=0)
        )

        self._lock_renovacao = threading.Lock()
        self._avisou_jwt = False
        super().__init__()

    # ------------------------------------------------------------------ lifecycle

    def close(self) -> None:
        """Close the HTTP client, but only if we own it."""
        if self._http_proprio:
            self._http.close()

    def __enter__(self) -> BlingClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"BlingClient(empresa={self.empresa!r}, enable_jwt={self.enable_jwt})"

    # ------------------------------------------------------------------ OAuth

    def url_autorizacao(self, state: str | None = None) -> tuple[str, str]:
        """Return ``(url, state)``. Send the user to the URL, then verify the state.

        ``redirect_uri`` and ``scope`` are not sent: Bling ignores them in the request and
        always uses what is registered on the app.
        """
        valor = state or gerar_state()
        return url_autorizacao(self.client_id, valor), valor

    def trocar_codigo(self, code: str) -> Token:
        """Exchange an authorization code for the token pair.

        The code is valid for **60 seconds**, so do not let anything slow happen between
        receiving it and calling this.
        """
        payload = self._post_oauth(OAUTH_TOKEN_URL, corpo_authorization_code(code))
        token = token_de_payload(payload, jwt=self.enable_jwt)
        self.tokens.set(self.empresa, token)
        logger.info(
            "token obtido para %s (expira em %.0fs, escopos=%d)",
            self.empresa,
            token.segundos_restantes(),
            len(token.escopos()),
        )
        return token

    def renovar_token(self) -> Token:
        """Force a refresh now, regardless of expiry."""
        return self._renovar(forcado=True)

    def revogar(
        self,
        token: str | None = None,
        tipo: str = "refresh_token",
        *,
        acao: str | None = None,
        alvo: str | None = None,
    ) -> None:
        """Revoke a token at ``POST /oauth/revoke``.

        ``acao`` (``logout`` | ``uninstall``) and ``alvo`` (``user`` | ``company``) widen
        the revocation far beyond the token given, and the effect cannot be undone -- every
        affected user has to go through the browser flow again. Both default to unset.
        """
        if token is None:
            atual = self.tokens.get(self.empresa)
            if atual is None:
                raise BlingSemToken(f"nenhum token guardado para a empresa {self.empresa!r}")
            token = atual.refresh_token if tipo == "refresh_token" else atual.access_token
        self._post_oauth(
            OAUTH_REVOKE_URL,
            corpo_revoke(token, tipo, revoke_action=acao, revoke_target=alvo),
            espera_json=False,
        )
        logger.info("token revogado para %s (tipo=%s, acao=%s, alvo=%s)",
                    self.empresa, tipo, acao, alvo)

    def _post_oauth(
        self,
        url: str,
        corpo: Mapping[str, str],
        *,
        espera_json: bool = True,
    ) -> dict[str, Any]:
        p = self.core.prepare_oauth(
            url, corpo, cabecalhos_token(self.client_id, self.client_secret,
                                         enable_jwt=self.enable_jwt)
        )
        self._limiter_token.acquire()
        # The OAuth endpoints also count against the account's 3 req/s budget.
        self._limiter.acquire()
        try:
            resp = self._http.request(p.method, p.url, data=p.data, headers=p.headers)
        except httpx.HTTPError as exc:
            raise BlingErroTransporte(f"POST {url} falhou (rede): {exc}") from exc

        if resp.status_code >= 400:
            try:
                payload = resp.json()
            except ValueError:
                payload = None
            raise _error_for(resp.status_code, payload, "POST", url)
        if not espera_json:
            return {}
        try:
            dados = resp.json()
        except ValueError as exc:
            raise BlingErroTransporte(
                f"POST {url} devolveu resposta nao-JSON (HTTP {resp.status_code})"
            ) from exc
        if not isinstance(dados, dict):
            raise BlingErroTransporte(f"POST {url} devolveu um corpo inesperado")
        return dados

    # ------------------------------------------------------------------ tokens

    def _access_token(self) -> str:
        token = self.tokens.get(self.empresa)
        if token is None:
            raise BlingSemToken(
                f"nenhum token guardado para a empresa {self.empresa!r}. "
                f"Rode `bling auth --empresa {self.empresa}` para autorizar o app."
            )
        if self.enable_jwt and not token.jwt and not self._avisou_jwt:
            self._avisou_jwt = True
            logger.warning(
                "o token guardado para %s foi emitido como token opaco (descontinuado pelo "
                "Bling); a proxima renovacao o promove a JWT",
                self.empresa,
            )
        if not token.precisa_renovar(self.folga_renovacao):
            return token.access_token
        return self._renovar().access_token

    def _renovar(self, *, forcado: bool = False) -> Token:
        """Refresh the access token, at most once per concurrent group of callers.

        Two layers of de-duplication, both needed:

        1. the in-process lock plus a double-checked re-read, so N worker threads produce
           **one** ``POST /oauth/token``;
        2. a transactional store holds *its* lock across read -> refresh -> write, so N
           processes do the same. Bling rotates the refresh token on use, so two processes
           racing a refresh leave one holding a token Bling has already invalidated -- and
           the only cure is re-authorizing by hand.
        """
        with self._lock_renovacao:
            atual = self.tokens.get(self.empresa)
            if atual is not None and not forcado and not atual.precisa_renovar(self.folga_renovacao):
                return atual  # another thread already refreshed while we waited

            if isinstance(self.tokens, TokenStoreTransacional):
                return self.tokens.atualizar(self.empresa, self._trocar_refresh)
            token = self._trocar_refresh(atual)
            self.tokens.set(self.empresa, token)
            return token

    def _trocar_refresh(self, atual: Token | None) -> Token:
        if atual is None or not atual.refresh_token:
            raise BlingSemToken(
                f"sem refresh_token para a empresa {self.empresa!r}. "
                f"Rode `bling auth --empresa {self.empresa}`."
            )
        payload = self._post_oauth(OAUTH_TOKEN_URL, corpo_refresh_token(atual.refresh_token))
        token = token_de_payload(payload, jwt=self.enable_jwt, anterior=atual)
        logger.info("token renovado para %s (expira em %.0fs)",
                    self.empresa, token.segundos_restantes())
        return token

    def dados_empresa(self) -> Any:
        """``GET /empresas/me/dados-basicos`` -- cheap, and how you discover the companyId
        that webhooks arrive under."""
        return self.request("GET", "empresas/me/dados-basicos")

    # ------------------------------------------------------------------ requests

    def request(
        self,
        metodo: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any | None = None,
        modelo: type[BaseModel] | None = None,
        lista_de: type[BaseModel] | None = None,
        idempotente: bool | None = None,
        headers: Mapping[str, str] | None = None,
        bruto: bool = False,
        timeout: float | None = None,
    ) -> Any:
        """Call any endpoint, including the ones this SDK does not model yet.

        This is the escape hatch that covers all 265 documented operations from day one,
        and every resource method is built on it. The ``{"data": ...}`` envelope is always
        unwrapped; pass ``bruto=True`` to get the raw ``httpx.Response`` instead.

        ``idempotente`` overrides the retry policy. Default: everything but POST is
        idempotent. Set it to ``False`` on a POST-like action you must never see repeated,
        or ``True`` on one you know is safe.
        """
        renovou = False
        ultimo: BaseException | None = None

        for tentativa in range(1, self.max_tentativas + 1):
            p = self.core.prepare(
                metodo,
                path,
                params=params,
                json=json,
                # Late-bound on purpose: a refresh triggered by a 401 below must be picked
                # up by the next attempt.
                access_token=self._access_token(),
                headers=headers,
                idempotente=idempotente,
            )
            self._limiter.acquire()
            try:
                resp = self._http.request(
                    p.method,
                    p.url,
                    params=p.params,
                    json=p.json,
                    headers=p.headers,
                    timeout=timeout if timeout is not None else httpx.USE_CLIENT_DEFAULT,
                )
            except httpx.HTTPError as exc:
                # A POST may have been applied server-side with only the response lost.
                # Retrying would double-post -- a second stock movement on POST /estoques.
                if not deve_repetir(None, idempotente=p.idempotente):
                    raise BlingErroTransporte(
                        f"{p.method} {path} falhou (rede): {exc}"
                    ) from exc
                ultimo = exc
                logger.warning("%s %s falhou (rede), tentativa %d: %s",
                               p.method, path, tentativa, exc)
                self._dormir(tentativa, None)
                continue

            if resp.status_code == 429:
                erro = _error_for(resp.status_code, self._json_ou_none(resp), p.method, path)
                periodo = getattr(erro, "periodo", "")
                if isinstance(erro, BlingLimiteDiario):
                    # 120.000/day is gone; waiting cannot help today.
                    raise erro
                espera = tempo_espera(tentativa, resp.headers.get("Retry-After"), self.teto_backoff)
                # Pause every thread, not just this one: the others are at full speed.
                self._limiter.penalize(espera)
                logger.warning("429 em %s %s; pausando %.1fs", p.method, path, espera)
                ultimo = erro
                if not deve_repetir(429, idempotente=p.idempotente, periodo_429=periodo):
                    raise erro
                # No sleep here: the next acquire() already blocks past the shared pause.
                continue

            if resp.status_code == 401 and not renovou:
                # A token can be revoked server-side before expires_at. One forced refresh.
                logger.info("401 em %s %s; forcando renovacao do token", p.method, path)
                self._renovar(forcado=True)
                renovou = True
                continue

            if resp.status_code >= 500 and deve_repetir(
                resp.status_code, idempotente=p.idempotente
            ):
                ultimo = _error_for(resp.status_code, self._json_ou_none(resp), p.method, path)
                logger.warning("%s em %s %s, tentativa %d",
                               resp.status_code, p.method, path, tentativa)
                self._dormir(tentativa, resp.headers.get("Retry-After"))
                continue

            return self.core.parse(
                resp, modelo, lista_de, bruto=bruto, metodo=p.method, path=path
            )

        assert ultimo is not None
        if isinstance(ultimo, httpx.HTTPError):
            raise BlingErroTransporte(
                f"{metodo.upper()} {path} falhou depois de {self.max_tentativas} tentativas: "
                f"{ultimo}"
            ) from ultimo
        raise ultimo

    def _dormir(self, tentativa: int, retry_after: str | None) -> None:
        """Back off before the next attempt -- but never after the last one.

        Sleeping on the final attempt only delays the exception the caller is already going
        to get, which on the default settings wastes 16 seconds per failed call.
        """
        if tentativa >= self.max_tentativas:
            return
        time.sleep(tempo_espera(tentativa, retry_after, self.teto_backoff))

    @staticmethod
    def _json_ou_none(resp: httpx.Response) -> dict[str, Any] | None:
        try:
            dados = resp.json()
        except ValueError:
            return None
        return dados if isinstance(dados, dict) else None


__all__ = ["BlingClient"]
