# bling-sdk

SDK Python para a [API v3 do Bling ERP](https://developer.bling.com.br).

```bash
pip install git+https://github.com/GabMalta/bling_sdk
```

## Primeiro uso

Autorize o app uma vez. Isso abre o navegador, captura o `?code=` num servidor local e grava
os tokens:

```bash
export BLING_CLIENT_ID=...
export BLING_CLIENT_SECRET=...
bling auth --empresa minha-loja
```

Depois disso o cliente cuida de tudo — renovação de token inclusive:

```python
from bling_sdk import BlingClient

with BlingClient(client_id="...", client_secret="...", empresa="minha-loja") as bling:
    for produto in bling.produtos.iter_todos(limite=100):
        print(produto.id, produto.nome, produto.preco)
```

## O que o cliente faz por você

- **Renova o token sozinho**, 5 minutos antes de expirar, e de forma deduplicada: oito
  threads causam uma única chamada a `/oauth/token`. Ver [Autenticação](auth.md).
- **Respeita 3 req/s por conta**, com janela deslizante e pausa global em caso de 429.
  Ver [Limites e retry](limites.md).
- **Desembrulha o envelope `{"data": ...}`** sempre — todo método devolve o conteúdo, nunca
  o envelope.
- **Repete o que é seguro repetir** e só isso: um `POST /estoques` que devolve 5xx **não** é
  repetido, porque o movimento pode ter sido lançado.
- **Valida intervalos de data** acima de um ano antes de gastar a requisição.

## Envelope e modelos

A API devolve `{"data": ...}`. O SDK sempre desembrulha:

```python
produto = bling.produtos.obter(123)      # -> Produto
produtos = bling.produtos.listar()       # -> list[Produto]
saldos = bling.estoques.saldos()         # -> list[Saldo]
```

Modelos usam `extra="allow"`, então um campo novo que o Bling adicione não quebra o parsing e
**sobrevive a um round-trip**:

```python
p = bling.produtos.obter(123)
p.preco = 19.90
bling.produtos.atualizar_parcial(123, {"preco": p.preco})
```

Nomes são português snake_case; o alias camelCase do wire é gerado automaticamente:

```python
p.descricao_curta     # <- descricaoCurta
p.id_produto_pai      # <- idProdutoPai
p.tributacao.n_fci    # <- nFCI
```

## Cobertura atual

Tipados com modelo e método dedicado:

| Módulo | Acesso |
|---|---|
| produtos (+ variações, estruturas, fornecedores, lojas) | `bling.produtos` |
| estoques (saldos e lançamentos) | `bling.estoques` |
| depósitos | `bling.depositos` |
| pedidos de venda | `bling.pedidos.vendas` |
| contatos | `bling.contatos` |
| NF-e | `bling.nfe` |
| situações e transições | `bling.situacoes` |
| categorias de produto | `bling.categorias.produtos` |
| canais de venda | `bling.canais_venda` |
| empresa | `bling.empresas` |

**Não implementados ainda:** contas a pagar/receber, NFC-e, NFS-e, logística e etiquetas,
pedidos de compra, propostas comerciais, ordens de produção e de serviço, anúncios, caixas,
borderôs, contratos, campos customizados, formas de pagamento, grupos de produtos, listas de
preço, naturezas de operação, vendedores, lotes de produto, notificações, contas contábeis,
documentos compartilhados, homologação.

## Escape hatch

As 265 operações da API estão acessíveis desde o primeiro dia, modeladas ou não:

```python
# um endpoint sem método dedicado
vendedores = bling.request("GET", "vendedores", params={"limite": 100})

# contas a receber de um período
contas = bling.request("GET", "contas/receber", params={
    "dataInicial": "2026-01-01", "dataFinal": "2026-01-31",
})

# a resposta crua, para download de arquivo
resp = bling.request("GET", "nfe/documento/CHAVE", bruto=True)
```

`request()` passa pelo mesmo rate limiter, pela mesma política de retry e pela mesma
validação de intervalo de datas que os métodos tipados. Também aceita `modelo=` e `lista_de=`
se você quiser validar a resposta num modelo seu.

## Alternativa: MCP Server oficial

Para uso conversacional (ChatGPT, Claude) o Bling publica um
[MCP Server oficial](https://developer.bling.com.br/mcp-server). Ele não é dependência deste
SDK e serve a outro propósito: consulta ad-hoc, não integração programática.
