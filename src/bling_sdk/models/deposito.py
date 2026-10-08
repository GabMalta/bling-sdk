"""Warehouse models."""

from __future__ import annotations

from .common import BlingModel


class Deposito(BlingModel):
    id: int | None = None
    descricao: str | None = None
    situacao: int | None = None
    padrao: bool | None = None
    desconsiderar_saldo: bool | None = None
