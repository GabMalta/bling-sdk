# Webhooks

## As quatro regras que decidem o desenho do seu handler

!!! danger "Responda 2xx em até 5 segundos"
    Acima disso o Bling considera falha e reenvia. **Enfileire, nunca processe inline.**

!!! warning "A entrega não é ordenada"
    Um `updated` pode chegar antes do `created` do mesmo registro. Não assuma sequência.

!!! warning "A entrega é duplicada"
    O mesmo evento pode chegar duas vezes. Ancore idempotência em `event_id`.

!!! warning "Após 3 dias de falha a configuração é desabilitada"
    O Bling tenta reenviar por até 3 dias, com intervalos crescentes. No fim, **desabilita a
    configuração do webhook** e só um humano religa no painel. Monitore seus 5xx.

## Verificando a assinatura

O header `X-Bling-Signature-256` traz `sha256=<hex>`, um HMAC-SHA256 do corpo com o
**client_secret** do app como chave.

```python
from bling_sdk import parse_evento

evento = parse_evento(corpo_bytes, assinatura=header, client_secret=CLIENT_SECRET)
```

!!! danger "Use os bytes crus da request"
    A API recebe `bytes`, nunca um dict, e isso não é capricho: re-serializar o JSON muda a
    ordem das chaves e o espaçamento, e portanto o digest. Se o seu framework já parseou o
    corpo, pegue o corpo bruto (`request.body` no Django, `request.get_data()` no Flask).

A verificação acontece **antes** do parsing do JSON, então um corpo forjado é recusado sem ser
interpretado. A comparação usa `hmac.compare_digest`.

## Django

```python
# views.py
import json
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from bling_sdk import BlingAssinaturaInvalida, parse_evento

@csrf_exempt
def bling_webhook(request):
    try:
        evento = parse_evento(
            request.body,
            assinatura=request.headers.get("X-Bling-Signature-256"),
            client_secret=settings.BLING_CLIENT_SECRET,
        )
    except BlingAssinaturaInvalida:
        return HttpResponseForbidden()

    # Enfileire e saia. 5 segundos e o limite, e processar aqui arrisca o reenvio.
    processar_evento_bling.delay(evento.model_dump(mode="json"))
    return HttpResponse(status=200)
```

```python
# tasks.py
@shared_task
def processar_evento_bling(bruto):
    from bling_sdk.models import EventoWebhook

    evento = EventoWebhook.model_validate(bruto)

    # Idempotencia: a entrega e duplicada.
    _, criado = EventoProcessado.objects.get_or_create(event_id=evento.event_id)
    if not criado:
        return

    payload = evento.payload()
    match (evento.recurso, evento.acao):
        case ("product", "deleted"):
            Produto.objects.filter(bling_id=payload.id).delete()
        case ("product", _):
            atualizar_produto(payload)
        case ("stock", _):
            registrar_saldo(payload)
```

## Flask

```python
from flask import Flask, request, abort
from bling_sdk import BlingAssinaturaInvalida, parse_evento

app = Flask(__name__)

@app.post("/bling/webhook")
def webhook():
    try:
        evento = parse_evento(
            request.get_data(),
            assinatura=request.headers.get("X-Bling-Signature-256"),
            client_secret=CLIENT_SECRET,
        )
    except BlingAssinaturaInvalida:
        abort(403)
    fila.enqueue(processar, evento.model_dump(mode="json"))
    return "", 200
```

## O envelope

```json
{
  "eventId": "01945027-150e-72b4-e7cf-4943a042cd9c",
  "date": "2025-01-10T12:18:46Z",
  "version": "v1",
  "event": "product.updated",
  "companyId": "d4475854366a36c86a37e792f9634a51",
  "data": { }
}
```

```python
evento.event_id     # idempotencia
evento.recurso      # "product"
evento.acao         # "updated"
evento.company_id   # hash de 32 chars -- str, nao int
evento.payload()    # modelo tipado conforme recurso + acao
```

## Recursos e ações

Antes de configurar um recurso, o app precisa ter o **escopo** correspondente marcado no
painel — sem o escopo o recurso nem aparece para configurar.

| recurso / escopo | payload |
|---|---|
| `order` | `PedidoVendaWebhook` |
| `product` | `ProdutoWebhook` |
| `stock` | `EstoqueWebhook` |
| `virtual_stock` | `EstoqueVirtualWebhook` |
| `product_supplier` | `ProdutoFornecedorWebhook` |
| `invoice` | `NotaFiscalWebhook` |
| `consumer_invoice` | `NotaFiscalWebhook` |

Ações: `created`, `updated`, `deleted`. Em **toda** ação `deleted` o payload traz apenas
`{"id": N}` — por isso `payload()` devolve `PayloadExcluido`.

!!! note "Situação \"excluído\" não é `deleted`"
    Mudar a `situacao` de um registro para excluído emite `updated`, não `deleted`. O
    `deleted` só vem numa remoção definitiva.

## Estoque físico x virtual

Os gatilhos são diferentes, não só o payload:

- **`stock`** dispara em lançamentos **físicos**: vendas, NF-e, tela de estoque.
- **`virtual_stock`** dispara em reservas de venda e em recálculo de saldo de produtos com
  composição.

`virtual_stock` é ativado automaticamente quando `stock` é, e herda a configuração dele.

!!! warning "`vinculo_complexo`"
    Quando `True`, mais de 200 produtos vinculados tiveram o estoque virtual atualizado. O
    payload **omite** esses produtos e você precisa reler os saldos pela API:

    ```python
    if payload.vinculo_complexo:
        saldos = bling.estoques.saldos(ids_produtos=[...])
    ```

## Multi-empresa

`companyId` é a chave de roteamento. Descubra o de cada conta com
`bling empresa --empresa <alias>` e mantenha o mapa:

```python
EMPRESAS = {"d4475854366a36c86a37e792f9634a51": "loja-a"}

empresa = EMPRESAS.get(evento.company_id)
if empresa is None:
    logger.warning("webhook de empresa desconhecida: %s", evento.company_id)
    return HttpResponse(status=200)   # 2xx, senao o Bling reenvia por 3 dias

bling = BlingClient(CLIENT_ID, CLIENT_SECRET, empresa=empresa)
```

Responda 2xx mesmo para um evento que você vai descartar — um 4xx entra no ciclo de
retentativas e, em 3 dias, desabilita a configuração.
