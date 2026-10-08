# PUT vs PATCH

Este é o footgun mais caro da API do Bling, e o desenho do SDK existe para torná-lo
inalcançável por acidente.

## O problema

`PUT` substitui o recurso **inteiro**. Todo campo que você não enviar é apagado ou volta ao
valor padrão, **sem recuperação**.

```http
PUT /produtos/123
{"nome": "Copo", "tipo": "P", "situacao": "A", "formato": "S", "preco": 19.90}
```

Esse PUT acaba de apagar, do produto 123: `descricaoCurta`, `descricaoComplementar`, `marca`,
`gtin`, `pesoLiquido`, `dimensoes`, `tributacao` (NCM, CEST, origem — tudo), `midia`, e **cada
campo customizado**. Não há lixeira.

`PATCH` altera só o que você mandar. Mas **nem todo endpoint tem PATCH**.

## Como o SDK expressa isso

| Bling | método no SDK |
|---|---|
| `PATCH /x/{id}` | `atualizar_parcial(id, dados)` |
| `PUT /x/{id}` | `substituir(id, dados, confirmar=True)` |

E, deliberadamente:

!!! tip "Não existe método chamado `atualizar`"
    ```pycon
    >>> bling.produtos.atualizar(123, {"preco": 19.90})
    AttributeError: 'Produtos' object has no attribute 'atualizar'
    ```
    O nome óbvio fica sem binding de propósito. Quem o digitar por distração leva um
    `AttributeError` e vai ler a documentação — em vez de um PUT silencioso que destruiu a
    tributação do produto.

`substituir()` sem `confirmar=True` levanta antes de fazer qualquer HTTP:

```pycon
>>> bling.produtos.substituir(123, {"nome": "Copo"})
BlingSubstituicaoNaoConfirmada: PUT produtos/123 substitui o recurso INTEIRO: todo campo
que voce nao enviar sera apagado ou zerado, sem recuperacao. ...
```

## Quais módulos têm PATCH

**Têm:** `produtos` (`atualizar_parcial`), e as situações de `produtos` e `contatos`.

**Não têm** — nesses, `substituir()` é a única atualização: `depositos`, `contatos` (o
contato em si), `nfe`, `pedidos.vendas`, `produtos.lojas`, `produtos.fornecedores`,
`produtos.estruturas`, `categorias.produtos`, `situacoes`, `situacoes.transicoes`, `estoques`.

## A receita segura para quem não tem PATCH

Leia, mude o objeto, mande de volta. Os modelos usam `extra="allow"` e serializam com
`exclude_unset`, então **tudo** que veio na leitura volta na escrita — inclusive campos que
este SDK ainda não modela:

```python
pedido = bling.pedidos.vendas.obter(123)
pedido.observacoes = "entregar depois das 14h"
bling.pedidos.vendas.substituir(123, pedido, confirmar=True)
```

Isso funciona porque:

- o modelo guarda todo campo que a resposta trouxe, modelado ou não;
- `bruto()` usa `exclude_unset=True`, então nada que você não tocou é omitido — e nada que
  você não tocou é enviado como `null`.

### Por que `exclude_unset` e não `exclude_none`

Com `exclude_none`, um campo de lista com default `[]` seria **enviado** como lista vazia. Um
`camposCustomizados: []` num PUT apaga todos os campos customizados do produto. Com
`exclude_unset`, um modelo recém-construído serializa para `{}`:

```pycon
>>> Produto().bruto()
{}
>>> Produto(preco=9.9).bruto()
{'preco': 9.9}
```

## Alterando só o preço numa loja

Caso real e comum, e `produtos/lojas` não tem PATCH:

```python
vinculo = bling.produtos.lojas.obter(id_produto_loja)
vinculo.preco = 29.90
bling.produtos.lojas.substituir(id_produto_loja, vinculo, confirmar=True)
```

Nunca monte o corpo à mão aqui. `{"preco": 29.90}` num PUT apagaria `codigo`,
`idProdutoLoja`, `categoriasProdutos` e os vínculos de marca e fornecedor da loja.

## Para produtos, prefira PATCH

```python
# bom
bling.produtos.atualizar_parcial(123, {"preco": 19.90})

# desnecessariamente arriscado
p = bling.produtos.obter(123)
p.preco = 19.90
bling.produtos.substituir(123, p, confirmar=True)
```

Em `PUT /produtos`, `nome`, `tipo`, `situacao` e `formato` são obrigatórios em toda chamada.
