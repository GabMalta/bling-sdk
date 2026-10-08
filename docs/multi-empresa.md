# Multi-empresa

Uma instalação pode falar com várias contas Bling. `empresa` é o apelido que você escolhe para
cada conta, e ele chaveia **duas** coisas:

- o **token store** — cada conta tem seu par de tokens;
- o **rate limiter** — o limite de 3 req/s é por conta.

```python
loja_a = BlingClient(CLIENT_ID, CLIENT_SECRET, empresa="loja-a")
loja_b = BlingClient(CLIENT_ID, CLIENT_SECRET, empresa="loja-b")
```

Contas diferentes recebem limiters independentes (compartilhar um cortaria a vazão pela
metade). Dois clientes da **mesma** empresa compartilham o mesmo limiter automaticamente.

Quem tem uma conta só nunca precisa digitar `empresa` — o padrão é `"default"`.

## Autorizando cada conta

```bash
bling auth --empresa loja-a
bling auth --empresa loja-b
bling info
```

O mesmo `client_id`/`client_secret` serve: o app é seu, a autorização é de cada conta.

## Descobrindo o `companyId`

Webhooks identificam a conta por `companyId`, um hash de 32 caracteres — não o id numérico da
empresa. Descubra o de cada conta e guarde o mapa:

```bash
bling empresa --empresa loja-a
```

```python
EMPRESAS_POR_COMPANY_ID = {
    "d4475854366a36c86a37e792f9634a51": "loja-a",
    "a1b2c3d4e5f60718293a4b5c6d7e8f90": "loja-b",
}

def cliente_do_evento(evento):
    empresa = EMPRESAS_POR_COMPANY_ID.get(evento.company_id)
    if empresa is None:
        return None
    return BlingClient(CLIENT_ID, CLIENT_SECRET, empresa=empresa)
```

!!! warning "Verifique o casamento antes de confiar"
    Que `GET /empresas/me/dados-basicos` devolva exatamente o mesmo string que o webhook
    carrega como `companyId` está afirmado num changelog, mas **não foi verificado contra a
    API real**. Rode `bling empresa` e compare com um webhook de verdade. Se não bater, o mapa
    tem de ser montado à mão.

## Vários processos

Com várias contas e vários processos, cada conta precisa do seu arquivo de estado:

```python
from bling_sdk import ArquivoRateLimiter

BlingClient(..., empresa=empresa, rate_limiter=ArquivoRateLimiter(empresa=empresa))
```

O caminho padrão já embute o apelido (`ratelimit-<empresa>.json`), então contas distintas não
disputam o mesmo arquivo.

## Um store, várias contas

Tanto o `JSONFileTokenStore` quanto o `DjangoTokenStore` guardam todas as empresas no mesmo
lugar, chaveadas por apelido:

```json
{
  "versao": 1,
  "empresas": {
    "loja-a": {"access_token": "...", "expires_at": 1767225600.0, "jwt": true},
    "loja-b": {"access_token": "...", "expires_at": 1767225600.0, "jwt": true}
  }
}
```

Compartilhar um store entre clientes é o esperado, e é o que dá deduplicação de renovação
entre eles.
