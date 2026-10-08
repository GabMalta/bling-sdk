"""A small advisory file lock, stdlib only.

Needed because two kinds of state must be shared across *processes*, not just threads:

* tokens -- Bling rotates the refresh_token on every use, so two processes racing a refresh
  destroy each other's authorization permanently;
* the rate-limit window -- the 3 req/s budget is per Bling account, so a cron job and a web
  worker hitting the same account must coordinate.

``fcntl.flock`` on POSIX, ``msvcrt.locking`` on Windows. Both are advisory and per-handle,
so this guards cooperating processes using this module, not an arbitrary writer.
"""

from __future__ import annotations

import os
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import IO

if sys.platform == "win32":
    import msvcrt
else:
    import fcntl


class TimeoutDeTrava(TimeoutError):
    """The lock could not be acquired within the timeout."""


def _travar(handle: IO[bytes]) -> None:
    if sys.platform == "win32":
        # Windows locks a byte range, not the file, and the range must be non-empty.
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
    else:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)


def _destravar(handle: IO[bytes]) -> None:
    if sys.platform == "win32":
        try:
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
    else:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@contextmanager
def trava(caminho: Path, *, timeout: float = 10.0, intervalo: float = 0.02) -> Iterator[None]:
    """Hold an exclusive lock on ``<caminho>.lock`` for the duration of the block.

    The lock is a sidecar file, never the data file itself: on Windows a locked handle
    blocks the ``os.replace`` that makes writes atomic.
    """
    arquivo = caminho.with_name(caminho.name + ".lock")
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    limite = time.monotonic() + timeout
    handle = open(arquivo, "a+b")  # noqa: SIM115 - closed in the finally below
    try:
        while True:
            try:
                handle.seek(0)
                _travar(handle)
                break
            except OSError:
                if time.monotonic() >= limite:
                    raise TimeoutDeTrava(
                        f"nao foi possivel travar {arquivo} em {timeout}s; outro processo "
                        "pode estar parado segurando a trava"
                    ) from None
                time.sleep(intervalo)
        try:
            yield
        finally:
            _destravar(handle)
    finally:
        handle.close()


def escrever_atomico(caminho: Path, conteudo: str, *, modo: int = 0o600) -> None:
    """Write via a temp file in the same directory plus ``os.replace``.

    Same directory matters: ``os.replace`` is only atomic within one filesystem. A crash
    mid-write therefore leaves the previous file intact rather than a truncated one -- and
    a truncated token file means a lost 30-day authorization.
    """
    caminho.parent.mkdir(parents=True, exist_ok=True)
    try:
        caminho.parent.chmod(0o700)
    except OSError:
        pass  # best effort; see docs/auth.md on Windows ACLs
    temporario = caminho.with_name(f".{caminho.name}.{os.getpid()}.tmp")
    try:
        with open(temporario, "w", encoding="utf-8") as fh:
            fh.write(conteudo)
            fh.flush()
            os.fsync(fh.fileno())
        try:
            os.chmod(temporario, modo)
        except OSError:
            pass
        os.replace(temporario, caminho)
    finally:
        if temporario.exists():
            try:
                temporario.unlink()
            except OSError:
                pass
