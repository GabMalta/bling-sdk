"""``/produtos`` and its subresources.

``client.produtos`` plus ``.variacoes``, ``.estruturas``, ``.fornecedores`` and ``.lojas``,
mirroring the URL layout.

Products are one of the few core modules that *do* support PATCH, so
``atualizar_parcial()`` is available here. Prefer it: ``substituir()`` is a full PUT and
wipes anything you leave out.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from datetime import date
from typing import Any

from ..config import LIMITE_PADRAO
from ..models import Produto, ProdutoFornecedor, ProdutoLoja
from ._base import Recurso, corpo, exigir_confirmacao


class ProdutoVariacoes(Recurso):
    """``/produtos/variacoes`` -- variation parents and their attributes."""

    prefixo = "produtos/variacoes"

    def obter_por_pai(self, id_produto_pai: int) -> Any:
        """GET /produtos/variacoes/{idProdutoPai} -> Produto (the parent plus children)."""
        return self._get(self._path(id_produto_pai), modelo=Produto)

    def gerar_combinacoes(self, dados: Mapping[str, Any]) -> Any:
        """POST /produtos/variacoes/atributos/gerar-combinacoes.

        Returns the cartesian product of the attributes given. Does **not** persist
        anything, so it is safe to call repeatedly -- marked idempotent for that reason.
        """
        return self._post(
            self._path("atributos", "gerar-combinacoes"), corpo(dados), idempotente=True
        )

    def renomear_atributos(self, id_produto_pai: int, dados: Mapping[str, Any]) -> Any:
        """PATCH /produtos/variacoes/{idProdutoPai}/atributos."""
        return self._patch(self._path(id_produto_pai, "atributos"), corpo(dados))


class ProdutoEstruturas(Recurso):
    """``/produtos/estruturas`` -- the component list of a composition product.

    There is no ``GET /produtos/estruturas``, so there is no ``listar()``: fetch one by id
    with :meth:`obter`, or read the ``estrutura`` block off a product.
    """

    prefixo = "produtos/estruturas"

    def obter(self, id_estrutura: int) -> Any:
        """GET /produtos/estruturas/{idProdutoEstrutura}."""
        return self._get(self._path(id_estrutura))

    def substituir(
        self, id_estrutura: int, dados: Mapping[str, Any], *, confirmar: bool = False
    ) -> Any:
        """PUT /produtos/estruturas/{idProdutoEstrutura} -- replaces the WHOLE structure."""
        exigir_confirmacao(confirmar, "PUT", self._path(id_estrutura))
        return self._put(self._path(id_estrutura), corpo(dados))

    def adicionar_componentes(self, id_estrutura: int, componentes: Any) -> Any:
        """POST /produtos/estruturas/{idProdutoEstrutura}/componentes."""
        return self._post(self._path(id_estrutura, "componentes"), corpo(componentes))

    def atualizar_parcial_componente(
        self, id_estrutura: int, id_componente: int, dados: Mapping[str, Any]
    ) -> Any:
        """PATCH /produtos/estruturas/{idProdutoEstrutura}/componentes/{idComponente}."""
        return self._patch(
            self._path(id_estrutura, "componentes", id_componente), corpo(dados)
        )

    def excluir_componentes(self, id_estrutura: int, ids: list[int]) -> Any:
        """DELETE /produtos/estruturas/{idProdutoEstrutura}/componentes."""
        return self._delete(self._path(id_estrutura, "componentes"), {"idsComponentes": ids})

    def excluir_muitas(self, ids: list[int]) -> Any:
        """DELETE /produtos/estruturas -- removes the structure of several products."""
        return self._delete(self.prefixo, {"idsProdutos": ids})


class ProdutoFornecedores(Recurso):
    """``/produtos/fornecedores`` -- product/supplier links, with cost and purchase price."""

    prefixo = "produtos/fornecedores"

    def listar(
        self,
        *,
        pagina: int = 1,
        limite: int = LIMITE_PADRAO,
        id_produto: int | None = None,
        id_fornecedor: int | None = None,
        codigo: str | None = None,
        **filtros: Any,
    ) -> Any:
        """GET /produtos/fornecedores -> list[ProdutoFornecedor]. One HTTP call."""
        return self._listar(
            self.prefixo,
            pagina=pagina,
            limite=limite,
            lista_de=ProdutoFornecedor,
            idProduto=id_produto,
            idFornecedor=id_fornecedor,
            codigo=codigo,
            **filtros,
        )

    def iter_todos(
        self, *, limite: int = LIMITE_PADRAO, max_paginas: int | None = None, **filtros: Any
    ) -> Iterator[Any]:
        """Lazy walk over every page. Does not take ``pagina`` -- it owns it."""
        return self._iterar(
            self.prefixo,
            limite=limite,
            max_paginas=max_paginas,
            lista_de=ProdutoFornecedor,
            **filtros,
        )

    def obter(self, id_produto_fornecedor: int) -> Any:
        """GET /produtos/fornecedores/{idProdutoFornecedor} -> ProdutoFornecedor."""
        return self._get(self._path(id_produto_fornecedor), modelo=ProdutoFornecedor)

    def criar(self, dados: ProdutoFornecedor | Mapping[str, Any]) -> Any:
        """POST /produtos/fornecedores -> ProdutoFornecedor."""
        return self._post(self.prefixo, corpo(dados), modelo=ProdutoFornecedor)

    def substituir(
        self,
        id_produto_fornecedor: int,
        dados: ProdutoFornecedor | Mapping[str, Any],
        *,
        confirmar: bool = False,
    ) -> Any:
        """PUT /produtos/fornecedores/{id} -- replaces the whole link. No PATCH exists."""
        exigir_confirmacao(confirmar, "PUT", self._path(id_produto_fornecedor))
        return self._put(
            self._path(id_produto_fornecedor), corpo(dados), modelo=ProdutoFornecedor
        )

    def excluir(self, id_produto_fornecedor: int) -> Any:
        """DELETE /produtos/fornecedores/{idProdutoFornecedor}."""
        return self._delete(self._path(id_produto_fornecedor))


class ProdutoLojas(Recurso):
    """``/produtos/lojas`` -- per-marketplace price, code and category for a product."""

    prefixo = "produtos/lojas"

    def listar(
        self,
        *,
        pagina: int = 1,
        limite: int = LIMITE_PADRAO,
        id_loja: int | None = None,
        id_produto: int | None = None,
        data_alteracao_inicial: date | str | None = None,
        data_alteracao_final: date | str | None = None,
        **filtros: Any,
    ) -> Any:
        """GET /produtos/lojas -> list[ProdutoLoja]. One HTTP call."""
        return self._listar(
            self.prefixo,
            pagina=pagina,
            limite=limite,
            lista_de=ProdutoLoja,
            idLoja=id_loja,
            idProduto=id_produto,
            dataAlteracaoInicial=data_alteracao_inicial,
            dataAlteracaoFinal=data_alteracao_final,
            **filtros,
        )

    def iter_todos(
        self, *, limite: int = LIMITE_PADRAO, max_paginas: int | None = None, **filtros: Any
    ) -> Iterator[Any]:
        return self._iterar(
            self.prefixo, limite=limite, max_paginas=max_paginas, lista_de=ProdutoLoja, **filtros
        )

    def obter(self, id_produto_loja: int) -> Any:
        """GET /produtos/lojas/{idProdutoLoja} -> ProdutoLoja."""
        return self._get(self._path(id_produto_loja), modelo=ProdutoLoja)

    def criar(self, dados: ProdutoLoja | Mapping[str, Any]) -> Any:
        """POST /produtos/lojas -> ProdutoLoja."""
        return self._post(self.prefixo, corpo(dados), modelo=ProdutoLoja)

    def substituir(
        self,
        id_produto_loja: int,
        dados: ProdutoLoja | Mapping[str, Any],
        *,
        confirmar: bool = False,
    ) -> Any:
        """PUT /produtos/lojas/{idProdutoLoja} -- replaces the whole link. No PATCH exists.

        To change only the price: ``obter()`` it, set ``preco``, then pass the object back
        with ``confirmar=True``. The model keeps every field it read, so nothing is lost.
        """
        exigir_confirmacao(confirmar, "PUT", self._path(id_produto_loja))
        return self._put(self._path(id_produto_loja), corpo(dados), modelo=ProdutoLoja)

    def excluir(self, id_produto_loja: int) -> Any:
        """DELETE /produtos/lojas/{idProdutoLoja}."""
        return self._delete(self._path(id_produto_loja))


class Produtos(Recurso):
    """``/produtos``."""

    prefixo = "produtos"

    def __init__(self, client: Any) -> None:
        super().__init__(client)
        self.variacoes = ProdutoVariacoes(client)
        self.estruturas = ProdutoEstruturas(client)
        self.fornecedores = ProdutoFornecedores(client)
        self.lojas = ProdutoLojas(client)

    def listar(
        self,
        *,
        pagina: int = 1,
        limite: int = LIMITE_PADRAO,
        criterio: int | None = None,
        tipo: str | None = None,
        nome: str | None = None,
        codigos: list[str] | None = None,
        gtins: list[str] | None = None,
        ids_produtos: list[int] | None = None,
        id_categoria: int | None = None,
        id_loja: int | None = None,
        id_componente: int | None = None,
        data_inclusao_inicial: date | str | None = None,
        data_inclusao_final: date | str | None = None,
        data_alteracao_inicial: date | str | None = None,
        data_alteracao_final: date | str | None = None,
        filtro_saldo_estoque: str | None = None,
        **filtros: Any,
    ) -> Any:
        """GET /produtos -> list[Produto]. **Exactly one** HTTP call.

        Date ranges wider than a year are refused client-side (Bling answers 400); use
        ``bling_sdk.fatiar_periodo`` to slice them.
        """
        return self._listar(
            self.prefixo,
            pagina=pagina,
            limite=limite,
            lista_de=Produto,
            criterio=criterio,
            tipo=tipo,
            nome=nome,
            codigos=codigos,
            gtins=gtins,
            idsProdutos=ids_produtos,
            idCategoria=id_categoria,
            idLoja=id_loja,
            idComponente=id_componente,
            dataInclusaoInicial=data_inclusao_inicial,
            dataInclusaoFinal=data_inclusao_final,
            dataAlteracaoInicial=data_alteracao_inicial,
            dataAlteracaoFinal=data_alteracao_final,
            filtroSaldoEstoque=filtro_saldo_estoque,
            **filtros,
        )

    def iter_todos(
        self, *, limite: int = LIMITE_PADRAO, max_paginas: int | None = None, **filtros: Any
    ) -> Iterator[Any]:
        """Walk the whole catalogue lazily, respecting the rate limiter.

        Takes the same filters as :meth:`listar` minus ``pagina``. Stops on the first short
        page; a last page that is exactly full costs one extra empty request.
        """
        return self._iterar(
            self.prefixo, limite=limite, max_paginas=max_paginas, lista_de=Produto, **filtros
        )

    def obter(self, id_produto: int) -> Any:
        """GET /produtos/{idProduto} -> Produto."""
        return self._get(self._path(id_produto), modelo=Produto)

    def criar(self, dados: Produto | Mapping[str, Any]) -> Any:
        """POST /produtos -> Produto.

        Not idempotent: a 5xx or a timeout is **not** retried, because Bling may have
        created the product and only lost the response.
        """
        return self._post(self.prefixo, corpo(dados), modelo=Produto)

    def atualizar_parcial(self, id_produto: int, dados: Produto | Mapping[str, Any]) -> Any:
        """PATCH /produtos/{idProduto} -> Produto. Only the fields you send change.

        This is the safe update. Prefer it over :meth:`substituir`.
        """
        return self._patch(self._path(id_produto), corpo(dados), modelo=Produto)

    def substituir(
        self, id_produto: int, dados: Produto | Mapping[str, Any], *, confirmar: bool = False
    ) -> Any:
        """PUT /produtos/{idProduto} -> Produto. Replaces the **whole** product.

        Every field you omit is wiped or reset to its default, with no recovery --
        ``descricaoCurta``, ``marca``, ``tributacao`` and every custom field included.
        ``nome``, ``tipo``, ``situacao`` and ``formato`` are required on every PUT.

        Products support PATCH, so you almost certainly want :meth:`atualizar_parcial`.
        ``confirmar=True`` is required here precisely so this cannot be reached by accident.
        """
        exigir_confirmacao(confirmar, "PUT", self._path(id_produto))
        return self._put(self._path(id_produto), corpo(dados), modelo=Produto)

    def excluir(self, id_produto: int) -> Any:
        """DELETE /produtos/{idProduto}."""
        return self._delete(self._path(id_produto))

    def excluir_muitos(self, ids: list[int]) -> Any:
        """DELETE /produtos -- removes several products by id."""
        return self._delete(self.prefixo, {"idsProdutos": ids})

    def alterar_situacao(self, id_produto: int, situacao: str) -> Any:
        """PATCH /produtos/{idProduto}/situacoes. ``situacao``: ``"A"`` or ``"I"``."""
        return self._patch(self._path(id_produto, "situacoes"), {"situacao": situacao})

    def alterar_situacoes(self, ids: list[int], situacao: str) -> Any:
        """POST /produtos/situacoes -- changes the status of several products at once."""
        return self._post(
            self._path("situacoes"), {"idsProdutos": ids, "situacao": situacao}
        )
