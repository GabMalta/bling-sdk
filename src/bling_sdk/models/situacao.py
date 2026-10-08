"""Status and status-transition models.

Bling models every module's state machine (orders, invoices, purchases) as ``situacoes``
belonging to a ``modulo``, plus ``transicoes`` between them. There is no ``GET /situacoes``
-- list them per module with ``client.situacoes.do_modulo(id)``.

The search index the endpoint inventory came from carries descriptions, not field schemas,
so the fields below are the ones confirmed from webhook payloads and endpoint descriptions.
``extra="allow"`` keeps everything else, so nothing is lost -- but read a real response
before relying on a named attribute here.
"""

from __future__ import annotations

from pydantic import Field

from .common import BlingModel, Ref


class Situacao(BlingModel):
    id: int | None = None
    nome: str | None = None
    #: The numeric value carried on orders and invoices. Confirmed via the pedido de venda
    #: webhook payload, which sends ``"situacao": {"id": N, "valor": N}``.
    valor: int | None = None


class AcaoModulo(BlingModel):
    id: int | None = None
    nome: str | None = None


class ModuloSistema(BlingModel):
    id: int | None = None
    nome: str | None = None
    situacoes: list[Situacao] = Field(default_factory=list)


class Transicao(BlingModel):
    id: int | None = None
    situacao_origem: Ref | None = None
    situacao_destino: Ref | None = None
    acoes: list[AcaoModulo] = Field(default_factory=list)
