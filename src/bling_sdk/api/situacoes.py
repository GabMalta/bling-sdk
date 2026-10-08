"""``/situacoes`` -- the status machine of every Bling module.

There is no ``GET /situacoes``, so no ``listar()``. Statuses belong to a module: list them
with :meth:`Situacoes.do_modulo`, after finding the module id via :meth:`Situacoes.modulos`.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..models import AcaoModulo, ModuloSistema, Situacao, Transicao
from ._base import Recurso, corpo, exigir_confirmacao


class SituacaoTransicoes(Recurso):
    """``/situacoes/transicoes`` -- the allowed moves between two statuses."""

    prefixo = "situacoes/transicoes"

    def obter(self, id_transicao: int) -> Any:
        """GET /situacoes/transicoes/{idTransicao} -> Transicao."""
        return self._get(self._path(id_transicao), modelo=Transicao)

    def criar(self, dados: Mapping[str, Any]) -> Any:
        """POST /situacoes/transicoes -> Transicao."""
        return self._post(self.prefixo, corpo(dados), modelo=Transicao)

    def substituir(
        self, id_transicao: int, dados: Mapping[str, Any], *, confirmar: bool = False
    ) -> Any:
        """PUT /situacoes/transicoes/{idTransicao} -- replaces the whole transition."""
        exigir_confirmacao(confirmar, "PUT", self._path(id_transicao))
        return self._put(self._path(id_transicao), corpo(dados), modelo=Transicao)

    def excluir(self, id_transicao: int) -> Any:
        """DELETE /situacoes/transicoes/{idTransicao}."""
        return self._delete(self._path(id_transicao))


class Situacoes(Recurso):
    """``/situacoes``."""

    prefixo = "situacoes"

    def __init__(self, client: Any) -> None:
        super().__init__(client)
        self.transicoes = SituacaoTransicoes(client)

    def modulos(self) -> Any:
        """GET /situacoes/modulos -> list[ModuloSistema]. Start here."""
        return self._get(self._path("modulos"), lista_de=ModuloSistema)

    def do_modulo(self, id_modulo: int) -> Any:
        """GET /situacoes/modulos/{idModuloSistema} -> ModuloSistema, with its statuses.

        This is the replacement for the ``listar()`` that does not exist.
        """
        return self._get(self._path("modulos", id_modulo), modelo=ModuloSistema)

    def acoes_do_modulo(self, id_modulo: int) -> Any:
        """GET /situacoes/modulos/{idModuloSistema}/acoes -> list[AcaoModulo]."""
        return self._get(self._path("modulos", id_modulo, "acoes"), lista_de=AcaoModulo)

    def transicoes_do_modulo(self, id_modulo: int) -> Any:
        """GET /situacoes/modulos/{idModuloSistema}/transicoes -> list[Transicao]."""
        return self._get(self._path("modulos", id_modulo, "transicoes"), lista_de=Transicao)

    def obter(self, id_situacao: int) -> Any:
        """GET /situacoes/{idSituacao} -> Situacao."""
        return self._get(self._path(id_situacao), modelo=Situacao)

    def criar(self, dados: Situacao | Mapping[str, Any]) -> Any:
        """POST /situacoes -> Situacao."""
        return self._post(self.prefixo, corpo(dados), modelo=Situacao)

    def substituir(
        self, id_situacao: int, dados: Situacao | Mapping[str, Any], *, confirmar: bool = False
    ) -> Any:
        """PUT /situacoes/{idSituacao} -- replaces the whole status. No PATCH exists."""
        exigir_confirmacao(confirmar, "PUT", self._path(id_situacao))
        return self._put(self._path(id_situacao), corpo(dados), modelo=Situacao)

    def excluir(self, id_situacao: int) -> Any:
        """DELETE /situacoes/{idSituacao}."""
        return self._delete(self._path(id_situacao))
