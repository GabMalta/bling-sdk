# Paginação

A API pagina com `pagina` (base 1) e `limite` (padrão 100). **Não devolve total nem cursor**,
então página curta ou vazia é o único sinal de fim.

## `listar()` versus `iter_todos()`

Os dois existem e não se confundem:

```python
# UMA chamada HTTP. O que você usa numa tela web.
primeira = bling.produtos.listar(pagina=1, limite=100)
len(primeira)          # funciona

# Lazy, pagina sozinho. NÃO aceita `pagina` -- ele é dono dela.
for produto in bling.produtos.iter_todos(limite=100):
    ...
```

`listar()` deliberadamente **não** pagina sozinho. Se paginasse, `len()` pararia de
funcionar, a contagem de requisições ficaria invisível, e um laço que queima a cota diária
pareceria uma list comprehension local.

`iter_todos()` é lazy: nada sai na rede antes do primeiro `next()`.

## Fim de dados

Como o Bling não devolve total, a iteração para na primeira página mais curta que `limite`.
Consequência documentada: quando a última página é **exatamente** cheia, há uma requisição
vazia extra para descobrir o fim.

```python
# 207 produtos, limite 100 -> 3 chamadas (100, 100, 7)
# 200 produtos, limite 100 -> 3 chamadas (100, 100, 0)
```

## Limitando

```python
for p in bling.produtos.iter_todos(limite=100, max_paginas=5):   # no máximo 500 itens
    ...
```

Filtros passam igual e são repetidos em toda página:

```python
for p in bling.produtos.iter_todos(tipo="P", id_categoria=123):
    ...
```

## Nomes por recurso

Plural concorda com o substantivo:

| recurso | iterador |
|---|---|
| produtos, depósitos, pedidos, contatos, canais de venda | `iter_todos()` |
| NF-e, categorias | `iter_todas()` |
| saldos de estoque | `iter_saldos()`, `iter_saldos_por_deposito()` |

## Intervalos de data acima de um ano

O Bling recusa com 400. O SDK valida **antes** de gastar a requisição, e `fatiar_periodo` faz
o corte:

```python
from datetime import date
from bling_sdk import fatiar_periodo

for inicio, fim in fatiar_periodo(date(2020, 1, 1), date(2026, 1, 1)):
    for pedido in bling.pedidos.vendas.iter_todos(data_inicial=inicio, data_final=fim):
        ...
```

As fatias são inclusivas e contíguas — cada uma começa no dia seguinte ao fim da anterior. O
passo padrão é 365 dias; `dias=` muda.

A validação é automática, o fatiamento é explícito: transformar uma chamada em quatorze em
silêncio é o tipo de surpresa que queima a cota diária.

## Paginando um endpoint não modelado

```python
from bling_sdk import iter_paginas

def buscar(*, pagina, limite, **filtros):
    return bling.request("GET", "contas/receber",
                         params={"pagina": pagina, "limite": limite, **filtros})

for conta in iter_paginas(buscar, limite=100, situacao=1):
    ...
```

## Ritmo

Toda página passa pelo rate limiter, então um `iter_todos()` sobre um catálogo grande anda a
~3 req/s e não toma 429. Um catálogo de 10.000 produtos com `limite=100` são 100 requisições,
~34 segundos. Se isso for rodar em paralelo com outro processo na mesma conta, use o
`ArquivoRateLimiter` — ver [Limites e retry](limites.md).
