"""Stock models.

Two different things share the word "estoque" in Bling and must not be confused:

* a **movement** (``POST /estoques``) -- an entry or exit that changes a balance. Not
  idempotent, never retried on 5xx.
* a **balance** (``GET /estoques/saldos``) -- what is on hand right now.
"""

from __future__ import annotations

from pydantic import Field

from .common import BlingModel, DataHora, Ref


class SaldoDeposito(BlingModel):
    """One warehouse's slice of a product's balance."""

    id: int | None = None
    #: What exists physically.
    saldo_fisico: float | None = None
    #: Physical minus sales reservations, plus composition maths.
    saldo_virtual: float | None = None


class Saldo(BlingModel):
    """A product's balance, totalled and per warehouse."""

    produto: Ref | None = None
    saldo_fisico_total: float | None = None
    saldo_virtual_total: float | None = None
    depositos: list[SaldoDeposito] = Field(default_factory=list)


class Estoque(BlingModel):
    """A stock movement.

    ``operacao`` is ``"E"`` for an entry (balance goes up) or ``"S"`` for an exit (down).
    """

    id: int | None = None
    produto: Ref | None = None
    deposito: Ref | None = None
    operacao: str | None = None
    preco: float | None = None
    custo: float | None = None
    quantidade: float | None = None
    observacoes: str | None = None
    data: DataHora | None = None
