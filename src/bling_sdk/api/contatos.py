"""``/contatos`` -- customers, suppliers, carriers and sales reps."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from datetime import date
from typing import Any

from ..config import LIMITE_PADRAO
from ..models import Contato, TipoContato
from ._base import Recurso, corpo, exigir_confirmacao


class Contatos(Recurso):
    """``/contatos``.

    The contact itself has no PATCH -- only its status does, via :meth:`alterar_situacao`.
    """

    prefixo = "contatos"

    def listar(
        self,
        *,
        pagina: int = 1,
        limite: int = LIMITE_PADRAO,
        pesquisa: str | None = None,
        criterio: int | None = None,
        id_tipo_contato: int | None = None,
        tipo_pessoa: str | None = None,
        numero_documento: str | None = None,
        data_inclusao_inicial: date | str | None = None,
        data_inclusao_final: date | str | None = None,
        data_alteracao_inicial: date | str | None = None,
        data_alteracao_final: date | str | None = None,
        **filtros: Any,
    ) -> Any:
        """GET /contatos -> list[Contato]. One HTTP call.

        ``tipo_pessoa``: ``"F"`` pessoa fisica, ``"J"`` pessoa juridica.
        """
        return self._listar(
            self.prefixo,
            pagina=pagina,
            limite=limite,
            lista_de=Contato,
            pesquisa=pesquisa,
            criterio=criterio,
            idTipoContato=id_tipo_contato,
            tipoPessoa=tipo_pessoa,
            numeroDocumento=numero_documento,
            dataInclusaoInicial=data_inclusao_inicial,
            dataInclusaoFinal=data_inclusao_final,
            dataAlteracaoInicial=data_alteracao_inicial,
            dataAlteracaoFinal=data_alteracao_final,
            **filtros,
        )

    def iter_todos(
        self, *, limite: int = LIMITE_PADRAO, max_paginas: int | None = None, **filtros: Any
    ) -> Iterator[Any]:
        return self._iterar(
            self.prefixo, limite=limite, max_paginas=max_paginas, lista_de=Contato, **filtros
        )

    def obter(self, id_contato: int) -> Any:
        """GET /contatos/{idContato} -> Contato."""
        return self._get(self._path(id_contato), modelo=Contato)

    def criar(self, dados: Contato | Mapping[str, Any]) -> Any:
        """POST /contatos -> Contato. Not idempotent; no 5xx retry."""
        return self._post(self.prefixo, corpo(dados), modelo=Contato)

    def substituir(
        self, id_contato: int, dados: Contato | Mapping[str, Any], *, confirmar: bool = False
    ) -> Any:
        """PUT /contatos/{idContato} -- replaces the whole contact. No PATCH exists.

        Read-modify-write: ``obter()``, mutate, pass the object back with ``confirmar=True``.
        """
        exigir_confirmacao(confirmar, "PUT", self._path(id_contato))
        return self._put(self._path(id_contato), corpo(dados), modelo=Contato)

    def excluir(self, id_contato: int) -> Any:
        """DELETE /contatos/{idContato}."""
        return self._delete(self._path(id_contato))

    def excluir_muitos(self, ids: list[int]) -> Any:
        """DELETE /contatos -- removes several contacts by id."""
        return self._delete(self.prefixo, {"idsContatos": ids})

    def consumidor_final(self) -> Any:
        """GET /contatos/consumidor-final -> Contato.

        The generic walk-in-customer record, used on NFC-e when there is no named buyer.
        """
        return self._get(self._path("consumidor-final"), modelo=Contato)

    def tipos(self) -> Any:
        """GET /contatos/tipos -> list[TipoContato]. Every contact type in the account."""
        return self._get(self._path("tipos"), lista_de=TipoContato)

    def tipos_do_contato(self, id_contato: int) -> Any:
        """GET /contatos/{idContato}/tipos -> list[TipoContato]."""
        return self._get(self._path(id_contato, "tipos"), lista_de=TipoContato)

    def alterar_situacao(self, id_contato: int, situacao: str) -> Any:
        """PATCH /contatos/{idContato}/situacoes.

        ``situacao``: ``"A"`` active, ``"I"`` inactive, ``"E"`` excluded. Moving a contact to
        excluded emits an ``updated`` webhook, not a ``deleted`` one.
        """
        return self._patch(self._path(id_contato, "situacoes"), {"situacao": situacao})

    def alterar_situacoes(self, ids: list[int], situacao: str) -> Any:
        """POST /contatos/situacoes -- changes the status of several contacts at once."""
        return self._post(self._path("situacoes"), {"idsContatos": ids, "situacao": situacao})
