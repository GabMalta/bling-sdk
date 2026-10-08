from ._base import Recurso, corpo, exigir_confirmacao
from .canais_venda import CanaisVenda
from .categorias import Categorias, CategoriasProdutos
from .contatos import Contatos
from .depositos import Depositos
from .empresas import Empresas
from .estoques import Estoques
from .nfe import Nfe
from .pedidos import Pedidos, PedidosVendas
from .produtos import (
    ProdutoEstruturas,
    ProdutoFornecedores,
    ProdutoLojas,
    Produtos,
    ProdutoVariacoes,
)
from .situacoes import SituacaoTransicoes, Situacoes

__all__ = [
    "CanaisVenda",
    "Categorias",
    "CategoriasProdutos",
    "Contatos",
    "Depositos",
    "Empresas",
    "Estoques",
    "Nfe",
    "Pedidos",
    "PedidosVendas",
    "ProdutoEstruturas",
    "ProdutoFornecedores",
    "ProdutoLojas",
    "ProdutoVariacoes",
    "Produtos",
    "Recurso",
    "SituacaoTransicoes",
    "Situacoes",
    "corpo",
    "exigir_confirmacao",
]
