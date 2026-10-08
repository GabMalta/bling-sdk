"""Rate limiting.

Bling allows 3 requests/second per **account** -- not per app, not per token -- counted
across every endpoint. Exceeding it yields 429, and a sustained excess gets the source IP
banned (300 errors in 10s, or 600 requests in 10s, each for 10 minutes).

So throttling belongs *inside* the SDK, above any transport-level retry. A retry that
happens below the limiter does not consume a slot and therefore amplifies the overrun --
the exact failure mode that forced a monkey-patch in the code this replaces.
"""

from __future__ import annotations

import json
import os
import threading
import time
from collections import deque
from pathlib import Path
from typing import Protocol

from ._filelock import escrever_atomico, trava
from .config import REQUISICOES_POR_SEGUNDO, caminho_ratelimit_padrao


class RateLimiter(Protocol):
    """Throttling contract.

    No ``release()``: the window is time-based, so there is nothing to give back.
    """

    def acquire(self) -> None:
        """Block until this caller may send a request."""
        ...

    def penalize(self, segundos: float) -> None:
        """Pause *every* caller for this long, after a 429."""
        ...


class JanelaDeslizanteRateLimiter:
    """At most ``max_chamadas`` per ``periodo`` window, with no bursts.

    Two constraints combined, because neither alone is enough:

    * **sliding window** -- spacing calls at a fixed ``periodo / max_chamadas`` would let 4
      calls fit inside one second (at 0, 1/3, 2/3 and 1.0);
    * **minimum interval** -- the sliding window alone releases ``max_chamadas`` instantly
      when the queue is empty, and the burst reaches the server in the same millisecond.

    ``penalize()`` pauses *all* threads: after a 429, slowing only the thread that received
    it changes nothing, because the others carry on at full speed.

    ``margem`` widens the window by a few percent. Without it calls sit exactly ``periodo``
    apart, and scheduling plus network jitter is enough for the next one to land inside the
    server's window -- and the server's clock is the one that counts, not ours.

    Ported from legitima_utils/alterar_preco_lojas/rate_limiter.py, algorithm unchanged.
    """

    def __init__(
        self,
        max_chamadas: int = REQUISICOES_POR_SEGUNDO,
        periodo: float = 1.0,
        margem: float = 0.05,
    ) -> None:
        if max_chamadas < 1:
            raise ValueError("max_chamadas deve ser >= 1")
        self._max_chamadas = int(max_chamadas)
        self._periodo = float(periodo) * (1.0 + margem)
        self._intervalo_minimo = self._periodo / self._max_chamadas
        self._lock = threading.Lock()
        self._slots: deque[float] = deque()
        self._pausado_ate = 0.0

    def _reservar(self) -> float:
        with self._lock:
            agora = time.monotonic()

            while self._slots and agora - self._slots[0] >= self._periodo:
                self._slots.popleft()

            candidatos = [agora, self._pausado_ate]

            if self._slots:
                candidatos.append(self._slots[-1] + self._intervalo_minimo)

            if len(self._slots) >= self._max_chamadas:
                candidatos.append(self._slots[0] + self._periodo)
                self._slots.popleft()

            slot = max(candidatos)
            self._slots.append(slot)
            return slot

    def acquire(self) -> None:
        while True:
            slot = self._reservar()

            # Sleep outside the lock: this thread already holds its reservation.
            espera = slot - time.monotonic()
            if espera > 0:
                time.sleep(espera)

            with self._lock:
                # No new penalty arrived while waiting, so it is safe to proceed.
                if time.monotonic() >= self._pausado_ate:
                    return

    def penalize(self, segundos: float) -> None:
        with self._lock:
            self._pausado_ate = max(self._pausado_ate, time.monotonic() + segundos)


class ArquivoRateLimiter:
    """Cross-process limiter coordinated through a small JSON file.

    Use this when more than one process talks to the same Bling account -- a cron job plus
    a web worker, or several gunicorn workers. The in-process limiter cannot see them, so
    together they would sail past 3 req/s and earn an IP ban.

    Uses ``time.time()``, not ``time.monotonic()``: monotonic clocks are not comparable
    across processes. The cost is sensitivity to wall-clock jumps (NTP steps, DST on some
    platforms); at 3 req/s a skew of a few hundred milliseconds is harmless.

    Composes an in-process limiter and acquires locally first, so a threaded process does
    not hammer the lock. One file-lock round-trip (~0.1-1 ms) per request is irrelevant at
    this rate.
    """

    def __init__(
        self,
        caminho: Path | str | None = None,
        max_chamadas: int = REQUISICOES_POR_SEGUNDO,
        periodo: float = 1.0,
        margem: float = 0.05,
        *,
        empresa: str = "default",
    ) -> None:
        self.caminho = Path(caminho) if caminho else caminho_ratelimit_padrao(empresa)
        self._max_chamadas = int(max_chamadas)
        self._periodo = float(periodo) * (1.0 + margem)
        self._intervalo_minimo = self._periodo / self._max_chamadas
        self._local = JanelaDeslizanteRateLimiter(max_chamadas, periodo, margem)

    def _ler(self) -> tuple[list[float], float]:
        if not self.caminho.exists():
            return [], 0.0
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8") or "{}")
        except (OSError, ValueError):
            # Rate-limit state is disposable: losing it costs at most one burst, so a
            # corrupt file is reset rather than raised. Tokens get the opposite treatment.
            return [], 0.0
        slots = dados.get("slots") or []
        pausado = dados.get("pausado_ate") or 0.0
        return (
            [float(s) for s in slots if isinstance(s, (int, float))],
            float(pausado) if isinstance(pausado, (int, float)) else 0.0,
        )

    def _escrever(self, slots: list[float], pausado_ate: float) -> None:
        escrever_atomico(
            self.caminho,
            json.dumps({"slots": slots, "pausado_ate": pausado_ate}),
            modo=0o600,
        )

    def _reservar(self) -> float:
        with trava(self.caminho, timeout=30.0):
            slots, pausado_ate = self._ler()
            agora = time.time()

            slots = [s for s in slots if agora - s < self._periodo]

            candidatos = [agora, pausado_ate]
            if slots:
                candidatos.append(slots[-1] + self._intervalo_minimo)
            if len(slots) >= self._max_chamadas:
                candidatos.append(slots[0] + self._periodo)
                slots.pop(0)

            slot = max(candidatos)
            slots.append(slot)
            self._escrever(sorted(slots), pausado_ate)
            return slot

    def acquire(self) -> None:
        self._local.acquire()
        while True:
            slot = self._reservar()
            espera = slot - time.time()
            if espera > 0:
                time.sleep(espera)
            _, pausado_ate = self._ler_rapido()
            if time.time() >= pausado_ate:
                return

    def _ler_rapido(self) -> tuple[list[float], float]:
        with trava(self.caminho, timeout=30.0):
            return self._ler()

    def penalize(self, segundos: float) -> None:
        self._local.penalize(segundos)
        with trava(self.caminho, timeout=30.0):
            slots, pausado_ate = self._ler()
            self._escrever(slots, max(pausado_ate, time.time() + segundos))


class SemLimite:
    """A no-op limiter. For tests, and for callers who throttle elsewhere."""

    def acquire(self) -> None:
        return None

    def penalize(self, segundos: float) -> None:
        return None


_registro: dict[str, RateLimiter] = {}
_registro_lock = threading.Lock()


def _rate_padrao() -> int:
    try:
        return max(1, int(os.environ.get("BLING_SDK_RATE_LIMIT", REQUISICOES_POR_SEGUNDO)))
    except ValueError:
        return REQUISICOES_POR_SEGUNDO


def limitador_padrao(empresa: str = "default") -> RateLimiter:
    """The process-wide limiter for one Bling account.

    Keyed per company because the 3 req/s budget is per account: two accounts need
    independent budgets (sharing one would halve throughput), while two ``BlingClient``
    instances on the *same* account must share one. ``BLING_SDK_RATE_LIMIT`` overrides the
    rate -- useful if Bling ever raises the limit for your app.
    """
    with _registro_lock:
        limiter = _registro.get(empresa)
        if limiter is None:
            limiter = JanelaDeslizanteRateLimiter(_rate_padrao())
            _registro[empresa] = limiter
        return limiter


def registrar_limitador(empresa: str, limiter: RateLimiter) -> None:
    """Install a custom limiter for a company -- a file-backed one, or a no-op in tests."""
    with _registro_lock:
        _registro[empresa] = limiter


def limpar_limitadores() -> None:
    """Drop every registered limiter. Test helper."""
    with _registro_lock:
        _registro.clear()
