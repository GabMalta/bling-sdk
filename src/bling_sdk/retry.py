"""Retry policy, as pure functions.

No client state, no sleeping, no I/O -- so the policy can be unit-tested without a client
and reused by an async client later.

**The per-verb rule.** GET, PUT, PATCH and DELETE retry on 429, 5xx and network errors,
because re-sending produces the same end state. POST retries on **429 only**: a 429 is
refused before processing, so the request provably did not take effect, while a 5xx or a
timeout on ``POST /estoques`` may mean Bling *did* post the stock movement and only the
response was lost. Retrying that inflates stock in a way nobody notices for weeks.

Ported in spirit from legitima_lojavirtual/bling/client.py.
"""

from __future__ import annotations

from .config import REQUISICOES_POR_SEGUNDO

TETO_BACKOFF = 30.0


def tempo_espera(tentativa: int, retry_after: str | None = None, teto: float = TETO_BACKOFF) -> float:
    """Seconds to wait before the next attempt.

    Honours ``Retry-After`` in seconds when Bling sends it; otherwise exponential backoff
    capped at ``teto``. The HTTP-date form of ``Retry-After`` is not handled -- it falls
    through to backoff rather than guessing at clock skew.
    """
    if retry_after:
        try:
            return max(0.0, min(float(retry_after), teto))
        except ValueError:
            pass
    return float(min(2**tentativa, teto))


def deve_repetir(
    status: int | None,
    *,
    idempotente: bool,
    periodo_429: str | None = None,
) -> bool:
    """Whether a failed attempt is worth repeating.

    ``status=None`` means a network-level failure (no response arrived).
    """
    if status == 429:
        # The daily budget is gone; waiting cannot help today. Fail fast and let the
        # caller reschedule instead of parking threads for hours.
        return periodo_429 != "day"
    if status is None:
        return idempotente
    if status >= 500:
        return idempotente
    return False


def espera_sugerida_por_segundo() -> float:
    """Fallback pause after a per-second 429, when no ``Retry-After`` is given."""
    return 1.0 / REQUISICOES_POR_SEGUNDO
