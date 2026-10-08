"""Product category models."""

from __future__ import annotations

from .common import BlingModel, Ref


class CategoriaProduto(BlingModel):
    id: int | None = None
    descricao: str | None = None
    #: The parent category; ``{"id": 0}`` means top level.
    categoria_pai: Ref | None = None
