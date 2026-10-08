"""Pagination helpers.

Bling pages with ``pagina`` (1-based) and ``limite`` (default 100). It returns no cursor
and no total count, so **a short or empty page is the only end-of-data signal**. A
documented consequence: when the last page happens to be exactly full, one extra empty
request is made to discover the end.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from datetime import date, timedelta
from typing import Any, TypeVar

from .config import INTERVALO_MAXIMO_FILTRO, LIMITE_PADRAO

T = TypeVar("T")


def iter_paginas(
    buscar: Callable[..., list[T]],
    *,
    limite: int = LIMITE_PADRAO,
    pagina_inicial: int = 1,
    max_paginas: int | None = None,
    **filtros: Any,
) -> Iterator[T]:
    """Walk every page, yielding items lazily.

    ``buscar`` is called as ``buscar(pagina=N, limite=L, **filtros)`` and must return a
    list. Iteration stops on the first page that comes back shorter than ``limite``.
    """
    pagina = pagina_inicial
    paginas_lidas = 0
    while True:
        itens = buscar(pagina=pagina, limite=limite, **filtros)
        yield from itens
        paginas_lidas += 1
        if len(itens) < limite:
            return
        if max_paginas is not None and paginas_lidas >= max_paginas:
            return
        pagina += 1


def fatiar_periodo(
    inicial: date,
    final: date,
    dias: int | None = None,
) -> Iterator[tuple[date, date]]:
    """Split a date range into slices Bling will accept.

    The one-year limit is *validated* automatically (see ``_core.validar_intervalo_datas``)
    but slicing is deliberately explicit: silently turning one call into fourteen is the
    kind of surprise that burns a daily quota.

    Slices are inclusive and contiguous -- each one starts the day after the previous ends.
    """
    if final < inicial:
        raise ValueError("final nao pode ser anterior a inicial")
    passo = timedelta(days=dias) if dias else INTERVALO_MAXIMO_FILTRO - timedelta(days=1)
    atual = inicial
    while atual <= final:
        fim = min(atual + passo, final)
        yield atual, fim
        atual = fim + timedelta(days=1)
