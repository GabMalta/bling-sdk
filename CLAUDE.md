# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Python SDK (sync only) for the Bling ERP API v3. Official docs: https://developer.bling.com.br
— but **do not WebFetch it**: the portal is a SPA that serves identical HTML for every path.
The full endpoint inventory (265 operations with verb, path, operationId and description) and
the extracted doc prose are checked in at `reference/ENDPOINTS.md` and `reference/ALL_DOCS.md`.
Read those instead; they are also the source of the test fixtures.

## Commands

Tooling is uv (if `uv` is not on PATH, use `python -m uv ...`).

- `uv sync` — install deps (dev group included)
- `uv run pytest` — all tests; single test:
  `uv run pytest tests/test_retry_client.py::test_post_nao_repete_500`
- `uv run ruff check .` — lint (E501 ignored); `uv run mypy` — strict type check of `src/`
- `uv run mkdocs serve` / `uv run mkdocs build --strict` — docs
- `uv run bling auth --empresa <alias>` — real OAuth round-trip, writes `tokens.json`

## Architecture

- `_core.py` — sans-IO `Core`: builds requests (`prepare`), normalizes query values, enforces
  the one-year date-filter guard, parses responses and errors (`parse`). **It must never
  perform I/O and never import `time.sleep`** — that is what keeps an async client a
  mechanical copy of one file. It also never renames a key: camelCase aliasing lives in the
  models, so there is exactly one aliasing boundary (`api/_base.corpo`).
- `client.py` — `BlingClient`, the only module that does I/O. Constructing it is free and
  silent: **no network, no token refresh, no filesystem write, no `print`, no `input`** (a
  test enforces this). `httpx.HTTPTransport(retries=0)` is deliberate — a transport retry sits
  below the rate limiter and the per-verb policy.
- `retry.py` — the policy as pure functions. **The rule that matters: GET/PUT/PATCH/DELETE
  retry on 429, 5xx and network errors; POST retries on 429 only.** A 429 is refused before
  processing, but a 5xx or timeout on `POST /estoques` may mean Bling posted the movement and
  lost only the response — retrying would inflate stock invisibly. A 429 with
  `period: "day"` is never retried.
- `ratelimit.py` — `RateLimiter` Protocol, a sliding-window + min-interval limiter (ported
  verbatim from `legitima_utils/alterar_preco_lojas/rate_limiter.py`; the algorithm is subtle
  and correct — don't "simplify" it), a cross-process file-backed one, and a registry keyed
  **per company** because Bling's 3 req/s is per account.
- `api/*.py` — resource groups (`client.produtos`, `.estoques`, `.pedidos.vendas`, …). Each
  method returns `self._c.request(...)`, typed `-> Any`. Nesting mirrors the URL.
- `models/*.py` — Pydantic v2 inheriting `BlingModel`: `extra="allow"` plus an
  `AliasGenerator` producing camelCase. `bruto()` uses **`exclude_unset`, not
  `exclude_none`** — a list field defaulting to `[]` would otherwise be sent, and
  `camposCustomizados: []` on a PUT wipes every custom field.
- `auth/` — `Token` (redacted `__repr__`; JWTs are live credentials up to 3000 chars),
  `TokenStore` Protocol plus the optional `TokenStoreTransacional`, three stores, and the
  `bling` CLI.
- `webhooks.py` — HMAC-SHA256 over the **raw request bytes** keyed by the client_secret.

## Conventions

- **Naming:** snake_case Portuguese, camelCase alias generated. Methods are Portuguese
  (`listar`, `obter`, `criar`, `atualizar_parcial`, `substituir`, `excluir`). Docstrings,
  comments and this file are English; README and `docs/` are Portuguese.
- **Add an endpoint:** a method in the right `api/<group>.py` using `_get`/`_post`/`_put`/
  `_patch`/`_delete` (paths are relative to `/Api/v3`; list params get a `[]` suffix
  automatically), optionally a model in `models/`, **plus a row in the `CHAMADAS` table in
  `tests/test_api.py`** — `test_tabela_cobre_toda_a_superficie_publica` fails if you forget.
  Take verb and path from `reference/ENDPOINTS.md`, never from memory.
- **Never add a method named `atualizar`.** PATCH is `atualizar_parcial`, PUT is
  `substituir(..., confirmar=True)`. Leaving the obvious short name unbound is what makes the
  data-wiping PUT unreachable by autocomplete. Every `substituir` calls
  `exigir_confirmacao()` before any HTTP.
- **Don't claim an endpoint that does not exist.** There is no `GET /situacoes`, no
  `GET /produtos/estruturas`, no `GET /estoques/{id}`, and no `DELETE /nfe/{id}` —
  `test_recursos_sem_listar_nao_mentem` guards this.
- **Tests mock HTTP with `respx`** against the real host. `tests/conftest.py` swaps the
  *name* `bling_sdk.client.time` for a fake — not `time.sleep`, which would patch sleeping
  process-wide and silently break the rate-limiter tests. Resource-path tests respond
  `{"data": {}}`, which satisfies both `modelo=` and `lista_de=`. Share the session-scoped
  `http` fixture: building an `httpx.Client` costs ~0.5s on Windows.
- **No tenant data in defaults.** The schemas this replaces baked in one company's `marca`,
  `categoria.id`, `ncm` and 140 lines of custom-field ids. Every model field is optional with
  a `None` or empty default.

## Not yet implemented

Reachable today via `client.request()`, each one mechanical to add: contas a pagar/receber,
NFC-e, NFS-e, logística/etiquetas, pedidos de compra, propostas comerciais, ordens de produção
e de serviço, anúncios, caixas, borderôs, contratos, campos customizados, formas de pagamento,
grupos de produtos, listas de preço, naturezas de operação, vendedores, `produtos/lotes`,
notificações, contas contábeis, documentos compartilhados, homologação.

## Unverified against the real API

Nothing here has run against a live Bling account yet. Treat these as open:

- whether `enable-jwt: 1` alongside an *opaque* token is accepted (the header is sent anyway;
  `Token.jwt` records how the token was minted and a WARNING fires on mismatch);
- the maximum accepted `limite` (documented default 100, ceiling never stated — passed through);
- whether query booleans want `"true"/"false"` or `1/0` (isolated in `_core._normalizar_params`);
- whether every module's array filters use the `[]` suffix (`idsProdutos[]`, `gtins[]` confirmed);
- whether Bling sends `Retry-After` on 429 (backoff covers both paths);
- what `GET /nfe/documento/{chaveAcesso}` returns and what its format param is called;
- whether `GET /empresas/me/dados-basicos` returns the same `companyId` webhooks carry;
- IP-block responses are presumably edge/WAF HTML, not the JSON envelope — `parse` degrades to
  `BlingErroTransporte`, untestable without earning a ban.

## Credentials

`client_id` and `client_secret` come only from constructor parameters or environment
variables — **never** hardcode them in a module, not even a `settings.py`. Tokens live
outside the package (`~/.config/bling-sdk/tokens.json` by default), never in
`site-packages`. Everything credential-shaped is masked by `redaction.py` before it reaches
a log line or an exception message, and `Token.__repr__` is redacted, so a 3000-character
JWT cannot leak through a traceback or a pytest diff.
