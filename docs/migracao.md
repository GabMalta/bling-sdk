# Migração

De `bling_api` (classe `BlingApi`) e de `legitima_lojavirtual/bling/client.py` para este SDK.

## Antes de começar

!!! danger "Rotacione as credenciais"
    `bling_api/bling_api/settings.py` tinha `CLIENT_ID` e `CLIENT_SECRET` em texto puro e
    commitados no git. Trate como comprometidos: gere novas credenciais no painel do Bling,
    revogue as antigas, e passe a lê-las de env.

## Diferenças que mudam o seu código

| | antes | agora |
|---|---|---|
| construir o cliente | renovava token na rede, imprimia em stdout, podia travar num `input()` | gratuito e silencioso |
| autorizar | `input()` ou `manage.py autorizar_bling` | `bling auth --empresa X` |
| tokens | `.txt` dentro de `site-packages` | `~/.config/bling-sdk/tokens.json` ou banco |
| renovação | a cada construção, sem checar expiração | preguiçosa, 5 min antes, deduplicada |
| JWT | não fazia | `enable-jwt: 1` por padrão |
| retorno | às vezes `{"data": ...}`, às vezes `data` | sempre o conteúdo |
| paginação | manual | `iter_todos()` |
| rate limit | fora do cliente, em 3 implementações | dentro, plugável |
| retry | urllib3 com POST na forcelist | por verbo, POST só em 429 |
| estender | subclassar e remendar | `client.request()` |

## Tabela de chamadas

### `BlingApi` para `BlingClient`

| antes | agora |
|---|---|
| `BlingApi()` | `BlingClient(client_id, client_secret, empresa="...")` |
| `.get_product(id)` | `.produtos.obter(id)` |
| `.get_products(params)` | `.produtos.listar(...)` / `.produtos.iter_todos(...)` |
| `.create_product(p)` | `.produtos.criar(p)` |
| `.edit_product(id, p)` | `.produtos.atualizar_parcial(id, p)` |
| `.delete_products(ids)` | `.produtos.excluir_muitos(ids)` |
| `.get_product_variacoes(id_pai)` | `.produtos.variacoes.obter_por_pai(id_pai)` |
| `.get_products_fornecedor()` | `.produtos.fornecedores.listar()` |
| `.create_product_fornecedor(f)` | `.produtos.fornecedores.criar(f)` |
| `.edit_product_fornecedor(id, f)` | `.produtos.fornecedores.substituir(id, f, confirmar=True)` |
| `.create_link_with_store(v)` | `.produtos.lojas.criar(v)` |
| `.create_estoque(e)` | `.estoques.criar(e)` ou `.estoques.lancar(...)` |
| `.get_depositos()` | `.depositos.listar()` |
| `.get_id_deposito()` | `.depositos.listar()` (a antiga só dava `print`) |
| `.get_nfs(situacao=)` | `.nfe.listar(situacao=...)` |
| `.get_nf(id)` | `.nfe.obter(id)` |
| `.put_nf(id, nf)` | `.nfe.substituir(id, nf, confirmar=True)` |
| `.get_contacts()` | `.contatos.listar()` / `.contatos.iter_todos()` |

Endpoints que os consumidores bolavam por subclasse:

| antes (em `BlingCustom`, `BlingEstoque`, ...) | agora |
|---|---|
| `GET produtos/lojas` | `.produtos.lojas.listar()` |
| `PUT produtos/lojas/{id}` | `.produtos.lojas.substituir(id, v, confirmar=True)` |
| `GET estoques/saldos/{idDeposito}` | `.estoques.saldos_por_deposito(id)` |
| `GET contas/receber` | `.request("GET", "contas/receber", params=...)` |
| `GET situacoes` | `.situacoes.do_modulo(id_modulo)` — não existe `GET /situacoes` |

### `legitima_lojavirtual.BlingClient`

| antes | agora |
|---|---|
| `BlingClient(token)` | `BlingClient(..., token_store=DjangoTokenStore(BlingToken))` |
| `.get(path, params)` | `.request("GET", path, params=params)` |
| `.trocar_codigo(code)` | `.trocar_codigo(code)` (igual) |
| `montar_url_autorizacao(state)` | `.url_autorizacao(state)` |
| `BlingNaoAutorizado` | `BlingSemToken` |
| `BlingSemPermissao` | `BlingSemPermissao` (igual, mensagem preservada) |
| `BlingError` | `BlingError` |
| `_throttle()` via Postgres | `rate_limiter=` com o seu limiter, ou `ArquivoRateLimiter` |
| `BlingToken.precisa_renovar()` | automático, dentro do cliente |

Ver [Django](django.md) para o wiring completo.

## Cuidados na conversão

### O envelope mudou

```python
# antes, inconsistente
resp = api.get_products(params)
produtos = resp["data"]        # em alguns metodos; em outros ja vinha desembrulhado

# agora, sempre o conteudo
produtos = bling.produtos.listar()
```

### `edit_product` era PATCH; `Produto.edit_product` era PUT

Os dois caminhos existiam, para a mesma operação. Hoje são métodos distintos e o PUT exige
confirmação:

```python
bling.produtos.atualizar_parcial(id, {"preco": 9.9})          # o antigo PATCH
bling.produtos.substituir(id, produto, confirmar=True)        # o antigo PUT
```

Ver [PUT vs PATCH](put-vs-patch.md) — é a parte mais importante desta migração.

### Defaults de tenant saíram dos schemas

`ProdutoSchema` embutia `marca="Legítima Textil"`, `categoria=Categoria(id=2432774)`,
`tributacao=Tributacao(ncm="5407.52.10", origem=2)`, `unidade="Mt"` e 140 linhas de
`camposCustomizados`. O `Produto` deste SDK não tem default nenhum.

Isso virou configuração da sua aplicação:

```python
# minhaapp/bling_defaults.py
from bling_sdk.models import Produto

PADRAO_TEXTIL = {
    "tipo": "P", "situacao": "A", "formato": "V", "unidade": "Mt",
    "marca": "Legítima Textil",
    "categoria": {"id": 2432774},
    "tributacao": {"ncm": "5407.52.10", "origem": 2},
}

def novo_produto(**campos):
    return Produto.model_validate({**PADRAO_TEXTIL, **campos})
```

Os ids de `camposCustomizados` são da conta: descubra com
`bling.request("GET", "campos-customizados")` em vez de manter a tabela à mão.

### `camposCustomizados` por índice

```python
# antes, e fragil: a ordem do template definia o significado
product["camposCustomizados"][3]["valor"] = quantidade
product["camposCustomizados"][7]["valor"] = composicao

# agora, por id
from bling_sdk.models import CampoCustomizado

campos = [
    CampoCustomizado(id_campo_customizado=2668618, valor=quantidade),
    CampoCustomizado(id_campo_customizado=2668622, valor=composicao),
]
```

### O host era diferente em dois lugares

`bling_api/bling.py` usava `api.bling.com.br`, `bling_api/produto.py` usava
`www.bling.com.br`. O correto para REST é `api.bling.com.br/Api/v3`; `www` só serve ao
`/oauth/authorize`. O SDK já usa cada um no lugar certo.

### O retry do urllib3 sai de cena

O `requests_policy` colocava POST, PUT, PATCH e DELETE na forcelist do urllib3, e
`altera_preco_multiloja.py` tinha de **desfazer** isso na mão, remontando o adapter da sessão
global. Nada disso é necessário: o SDK usa `httpx.HTTPTransport(retries=0)` e decide o retry
acima do rate limiter. Remova o monkey-patch.

## Ordem sugerida

1. Rotacione as credenciais.
2. `bling auth --empresa <alias>`, e confira com `bling info`.
3. Converta **leituras** primeiro — são reversíveis.
4. Depois as escritas, conferindo PUT x PATCH caso a caso.
5. Mova os defaults de tenant para a sua aplicação.
6. Troque o throttle próprio pelo do SDK e remova o monkey-patch do `requests_policy`.
7. Apague `legitima_lojavirtual/bling/client.py` e a dependência git de `bling_utils`.
