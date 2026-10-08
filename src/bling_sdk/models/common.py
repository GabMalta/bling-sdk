"""Base model and shared field types.

Bling's wire format is Portuguese camelCase (``descricaoCurta``, ``idProdutoPai``). Field
names here are the same vocabulary, snake_cased, and the camelCase alias is generated
automatically -- which removes roughly two hundred hand-written ``Field(alias=...)`` lines
and keeps the two spellings from drifting apart. Only irregular acronyms (``nFCI``,
``codigoANP``, ``imagemURL``) need an explicit override.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Any

from pydantic import AliasGenerator, BaseModel, ConfigDict, PlainSerializer

from ..config import FORMATO_DATA, FORMATO_DATA_HORA


def para_camel(nome: str) -> str:
    """``descricao_curta`` -> ``descricaoCurta``. Trailing underscores are stripped."""
    partes = nome.rstrip("_").split("_")
    return partes[0] + "".join(p.title() for p in partes[1:])


class BlingModel(BaseModel):
    """Base for every model.

    ``extra="allow"`` is load-bearing: Bling ships new fields continuously (``duns`` was
    added to products in a recent release), and an unknown field must never break parsing
    of a response the caller otherwise needs. Unknown fields also survive a
    ``model_dump(by_alias=True)`` round-trip, so reading a resource and writing it back
    does not silently drop what this SDK has not modelled yet.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        alias_generator=AliasGenerator(
            validation_alias=para_camel,
            serialization_alias=para_camel,
        ),
    )

    def bruto(self) -> dict[str, Any]:
        """The wire body: camelCase keys, with fields the caller never touched omitted.

        ``exclude_unset`` rather than ``exclude_none``, and the difference matters a lot on
        PUT. A list field defaulting to ``[]`` would otherwise be *sent* as an empty list,
        and ``camposCustomizados: []`` on a PUT wipes every custom field on the product.

        The semantics this gives are exactly right in both directions: a model parsed from a
        GET has every returned field marked as set, so read-modify-write preserves what this
        SDK has not modelled; a model built as ``Produto(preco=9.9)`` sends only ``preco``.
        """
        return self.model_dump(by_alias=True, exclude_unset=True)

    def __getitem__(self, chave: str) -> Any:
        return getattr(self, chave)


class Ref(BlingModel):
    """The ``{"id": N}`` shape Bling uses for every reference.

    Appears as ``categoria``, ``contato``, ``loja``, ``vendedor``, ``deposito``,
    ``naturezaOperacao`` and a dozen more.
    """

    id: int | None = None


#: Bling emits and accepts "2024-09-27", never a datetime, for plain date fields.
Data = Annotated[date, PlainSerializer(lambda v: v.strftime(FORMATO_DATA), return_type=str)]

#: Bling emits "2024-09-27 11:24:56" -- a space, not the ISO "T". Pydantic's default
#: serializer would write the T back and Bling rejects it.
DataHora = Annotated[
    datetime, PlainSerializer(lambda v: v.strftime(FORMATO_DATA_HORA), return_type=str)
]
