# bling-sdk

SDK Python para a [API v3 do Bling ERP](https://developer.bling.com.br).

OAuth 2.0 com renovação automática e deduplicada, respeito ao limite de 3 req/s por conta,
retry por verbo, paginação automática, modelos Pydantic para os recursos principais,
verificação de assinatura de webhook e CLI de autorização.

Requer Python 3.10+. Depende apenas de `httpx` e `pydantic`.

## Instalação

```bash
pip install git+https://github.com/GabMalta/bling_sdk
```

## Uso

Autorize o app uma vez — isso abre o navegador, captura o `?code=` e grava os tokens:

```bash
export BLING_CLIENT_ID=...
export BLING_CLIENT_SECRET=...
bling auth --empresa minha-loja
```

Depois o cliente cuida de tudo, renovação de token inclusive:

```python
from bling_sdk import BlingClient

with BlingClient(client_id="...", client_secret="...", empresa="minha-loja") as bling:
    for produto in bling.produtos.iter_todos(limite=100):
        print(produto.id, produto.nome, produto.preco)

    bling.produtos.atualizar_parcial(123, {"preco": 19.90})

    saldos = bling.estoques.saldos(ids_produtos=[123, 456])

    bling.estoques.lancar(123, operacao="E", quantidade=10, id_deposito=99)
```

## O que o cliente faz por você

- **Renova o token** 5 minutos antes de expirar, de forma deduplicada em processo e entre
  processos. O refresh token do Bling rota a cada uso, e duas renovações concorrentes
  destruiriam a autorização.
- **Respeita 3 req/s por conta**, com janela deslizante, intervalo mínimo e pausa global em
  429. Também protege o endpoint `/oauth/token`, cujo estouro rende 60 minutos de bloqueio
  de IP.
- **Desembrulha `{"data": ...}`** sempre — nenhum método devolve o envelope.
- **Repete só o que é seguro repetir:** um `POST /estoques` que devolve 5xx **não** é
  repetido, porque o movimento pode ter sido lançado e só a resposta perdida.
- **Manda `enable-jwt: 1`** por padrão; o token opaco está descontinuado pelo Bling.
- **Valida intervalos de data** acima de um ano antes de gastar a requisição.
- **Torna o PUT destrutivo difícil de disparar:** não existe método `atualizar`, e
  `substituir()` exige `confirmar=True`.

## Cobertura atual

| Módulo | Acesso |
| --- | --- |
| produtos (+ variações, estruturas, fornecedores, lojas) | `bling.produtos` |
| estoques (saldos e lançamentos) | `bling.estoques` |
| depósitos | `bling.depositos` |
| pedidos de venda | `bling.pedidos.vendas` |
| NF-e | `bling.nfe` |
| contatos | `bling.contatos` |
| situações e transições | `bling.situacoes` |
| categorias de produto | `bling.categorias.produtos` |
| canais de venda | `bling.canais_venda` |
| empresa | `bling.empresas` |

**Não implementados ainda:** contas a pagar/receber, NFC-e, NFS-e, logística e etiquetas,
pedidos de compra, propostas comerciais, ordens de produção e de serviço, anúncios, caixas,
borderôs, contratos, campos customizados, formas de pagamento, grupos de produtos, listas de
preço, naturezas de operação, vendedores, lotes de produto, notificações, contas contábeis,
documentos compartilhados, homologação.

Todos acessíveis desde já pelo escape hatch, que passa pelo mesmo rate limiter e pela mesma
política de retry:

```python
contas = bling.request("GET", "contas/receber", params={
    "dataInicial": "2026-01-01", "dataFinal": "2026-01-31",
})
```

## Documentação

```bash
uv run mkdocs serve
```

- [Autenticação](docs/auth.md) — OAuth, JWT, token stores
- [Limites e retry](docs/limites.md) — 3 req/s, bloqueios de IP, política por verbo
- [PUT vs PATCH](docs/put-vs-patch.md) — **leia antes de escrever qualquer coisa**
- [Paginação](docs/paginacao.md)
- [Webhooks](docs/webhooks.md)
- [CLI](docs/cli.md)
- [Django](docs/django.md)
- [Multi-empresa](docs/multi-empresa.md)
- [Migração](docs/migracao.md) — de `bling_api` e do cliente do `legitima_lojavirtual`

## Desenvolvimento

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy
uv run mkdocs build --strict
```

`reference/ENDPOINTS.md` traz as 265 operações da API com verbo, path e operationId, extraídas
da documentação oficial — é a fonte para adicionar endpoints.

## Status

O fluxo OAuth já foi validado contra uma conta real: `bling auth` completa o round-trip e
emite um JWT RS256. Os endpoints de recurso ainda não foram exercitados contra dados reais —
`CLAUDE.md` lista os pontos em aberto.
