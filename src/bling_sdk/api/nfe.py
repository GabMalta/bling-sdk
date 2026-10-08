"""``/nfe`` -- electronic invoices."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from datetime import date
from typing import Any

from ..config import LIMITE_PADRAO
from ..models import NotaFiscal
from ._base import Recurso, corpo, exigir_confirmacao


class Nfe(Recurso):
    """``/nfe``.

    Note there is no ``DELETE /nfe/{id}``: Bling only exposes the collection delete, so this
    class has :meth:`excluir_muitas` and no ``excluir``.
    """

    prefixo = "nfe"

    def listar(
        self,
        *,
        pagina: int = 1,
        limite: int = LIMITE_PADRAO,
        tipo: int | None = None,
        situacao: int | None = None,
        numero: str | None = None,
        serie: str | None = None,
        chave_acesso: str | None = None,
        id_contato: int | None = None,
        data_emissao_inicial: date | str | None = None,
        data_emissao_final: date | str | None = None,
        **filtros: Any,
    ) -> Any:
        """GET /nfe -> list[NotaFiscal]. One HTTP call. ``tipo``: 0 entrada, 1 saida."""
        return self._listar(
            self.prefixo,
            pagina=pagina,
            limite=limite,
            lista_de=NotaFiscal,
            tipo=tipo,
            situacao=situacao,
            numero=numero,
            serie=serie,
            chaveAcesso=chave_acesso,
            idContato=id_contato,
            dataEmissaoInicial=data_emissao_inicial,
            dataEmissaoFinal=data_emissao_final,
            **filtros,
        )

    def iter_todas(
        self, *, limite: int = LIMITE_PADRAO, max_paginas: int | None = None, **filtros: Any
    ) -> Iterator[Any]:
        return self._iterar(
            self.prefixo, limite=limite, max_paginas=max_paginas, lista_de=NotaFiscal, **filtros
        )

    def obter(self, id_nota: int) -> Any:
        """GET /nfe/{idNotaFiscal} -> NotaFiscal.

        ``link_danfe`` and ``link_pdf`` in the response carry an ``accessKey`` parameter --
        treat them as credentials and keep them out of logs.
        """
        return self._get(self._path(id_nota), modelo=NotaFiscal)

    def criar(self, dados: NotaFiscal | Mapping[str, Any]) -> Any:
        """POST /nfe -> NotaFiscal. Creates the invoice **without** transmitting it."""
        return self._post(self.prefixo, corpo(dados), modelo=NotaFiscal)

    def substituir(
        self, id_nota: int, dados: NotaFiscal | Mapping[str, Any], *, confirmar: bool = False
    ) -> Any:
        """PUT /nfe/{idNotaFiscal} -- replaces the whole invoice. No PATCH exists."""
        exigir_confirmacao(confirmar, "PUT", self._path(id_nota))
        return self._put(self._path(id_nota), corpo(dados), modelo=NotaFiscal)

    def excluir_muitas(self, ids: list[int]) -> Any:
        """DELETE /nfe -- removes several invoices by id.

        Bling exposes no per-id delete, which is why there is no ``excluir()``.
        """
        return self._delete(self.prefixo, {"idsNotas": ids})

    def enviar(self, id_nota: int, **extra: Any) -> Any:
        """POST /nfe/{idNotaFiscal}/enviar -- transmits the invoice to Sefaz.

        **Irreversible.** Once accepted, the invoice exists in the tax authority's records
        and the only way back is a cancellation or a devolution, both with their own legal
        deadlines. Not idempotent: never retried on a 5xx, and a transport error here means
        you must check the invoice's ``situacao`` before doing anything else.
        """
        return self._post(self._path(id_nota, "enviar"), dict(extra) or None)

    def lancar_contas(self, id_nota: int) -> Any:
        """POST /nfe/{idNotaFiscal}/lancar-contas. Not idempotent."""
        return self._post(self._path(id_nota, "lancar-contas"))

    def estornar_contas(self, id_nota: int) -> Any:
        """POST /nfe/{idNotaFiscal}/estornar-contas."""
        return self._post(self._path(id_nota, "estornar-contas"))

    def lancar_estoque(self, id_nota: int, id_deposito: int | None = None) -> Any:
        """POST /nfe/{idNotaFiscal}/lancar-estoque[/{idDeposito}]. Not idempotent."""
        partes: list[Any] = [id_nota, "lancar-estoque"]
        if id_deposito is not None:
            partes.append(id_deposito)
        return self._post(self._path(*partes))

    def estornar_estoque(self, id_nota: int) -> Any:
        """POST /nfe/{idNotaFiscal}/estornar-estoque."""
        return self._post(self._path(id_nota, "estornar-estoque"))

    def obter_documento(self, chave_acesso: str, *, bruto: bool = False, **extra: Any) -> Any:
        """GET /nfe/documento/{chaveAcesso} -- downloads the NF-e document.

        Whether this returns the file bytes or a JSON link, and what the format parameter is
        called, is not documented clearly. ``extra`` is passed through as query params, and
        ``bruto=True`` gives you the raw ``httpx.Response`` so you can inspect
        ``content-type`` and ``content`` yourself. Verify against the real API before relying
        on a particular shape.
        """
        return self._get(
            self._path("documento", chave_acesso), dict(extra) or None, bruto=bruto
        )
