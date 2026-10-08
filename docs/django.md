# Django

O SDK não depende de Django. O adapter abaixo é opcional e existe para um projeto Django
guardar tokens no banco que já tem.

## Instalação

```bash
pip install "bling-sdk[django] @ git+https://github.com/GabMalta/bling-sdk"
```

## Modelo

```python
# minhaapp/models.py
from bling_sdk.auth.django_store import BlingTokenBase

class BlingToken(BlingTokenBase):
    pass
```

```bash
python manage.py makemigrations minhaapp && python manage.py migrate
```

`BlingTokenBase` é abstrato e traz `empresa` (único, indexado), `access_token`,
`refresh_token`, `expires_at`, `token_type`, `scope`, `jwt`, `obtido_em` e `atualizado_em`.

!!! note "Os campos de token são `TextField`"
    JWTs têm 1.500 a 3.000 caracteres. Um `CharField(max_length=255)` truncaria a credencial.

## Wiring

```python
# minhaapp/bling.py
from django.conf import settings
from bling_sdk import BlingClient
from bling_sdk.auth.django_store import DjangoTokenStore
from minhaapp.models import BlingToken

def cliente(empresa: str = "default") -> BlingClient:
    return BlingClient(
        settings.BLING_CLIENT_ID,
        settings.BLING_CLIENT_SECRET,
        empresa=empresa,
        token_store=DjangoTokenStore(BlingToken),
    )
```

Credenciais vêm de env via `settings`, nunca de código:

```python
# settings.py
BLING_CLIENT_ID = os.environ["BLING_CLIENT_ID"]
BLING_CLIENT_SECRET = os.environ["BLING_CLIENT_SECRET"]
```

Construir o cliente é gratuito — sem rede, sem I/O —, então criar um por request é
aceitável. O que **não** é gratuito é o `httpx.Client` (carrega o certificado do sistema); se
isso aparecer no perfil, injete um compartilhado:

```python
import httpx
_HTTP = httpx.Client(timeout=30.0, transport=httpx.HTTPTransport(retries=0))

def cliente(empresa="default"):
    return BlingClient(..., http_client=_HTTP)
```

Um `http_client` injetado pertence a você: `close()` não o fecha.

## Autorização

O CLI resolve, e o token vai para o banco porque o store é o mesmo:

```bash
BLING_CLIENT_ID=... BLING_CLIENT_SECRET=... bling auth --empresa minha-loja
```

Se preferir dentro do Django, uma view de callback:

```python
# views.py
from django.shortcuts import redirect
from minhaapp.bling import cliente

def bling_autorizar(request):
    bling = cliente()
    url, state = bling.url_autorizacao()
    request.session["bling_state"] = state
    return redirect(url)

def bling_callback(request):
    import hmac
    esperado = request.session.pop("bling_state", "")
    recebido = request.GET.get("state", "")
    if not esperado or not hmac.compare_digest(recebido, esperado):
        return HttpResponseForbidden("state divergente")
    # O code expira em 60s: troque agora, sem fila no meio.
    cliente().trocar_codigo(request.GET["code"])
    return redirect("/admin/")
```

## Concorrência

`DjangoTokenStore` implementa `atualizar()`, então a renovação é deduplicada entre processos
via `select_for_update()` dentro de `transaction.atomic()`.

Isso não é opcional: o refresh token do Bling **rota a cada uso**, e dois workers renovando ao
mesmo tempo deixam um deles com um token que o Bling já invalidou.

!!! warning "Exige lock de linha no banco"
    PostgreSQL e MySQL suportam. **No SQLite o Django ignora `select_for_update()`** e você
    fica só com o lock em processo — suficiente para threads, não para múltiplos processos.

## Rate limiting entre workers

O limiter padrão é por processo. Com gunicorn em vários workers na mesma conta Bling, os 3
req/s são estourados em conjunto:

```python
from bling_sdk import ArquivoRateLimiter

BlingClient(..., rate_limiter=ArquivoRateLimiter(empresa=empresa))
```

Se você já coordena isso por tabela no Postgres, injete o seu — qualquer objeto com
`acquire()` e `penalize(segundos)` serve:

```python
class LimiterPostgres:
    def acquire(self): ...
    def penalize(self, segundos): ...
```

## Admin

```python
# admin.py
from django.contrib import admin
from minhaapp.models import BlingToken

@admin.register(BlingToken)
class BlingTokenAdmin(admin.ModelAdmin):
    # Nunca exponha access_token/refresh_token no admin.
    list_display = ("empresa", "expira_em_horas", "jwt", "atualizado_em")
    readonly_fields = ("empresa", "expires_at", "jwt", "scope", "atualizado_em")
    exclude = ("access_token", "refresh_token")

    @admin.display(description="expira em (h)")
    def expira_em_horas(self, obj):
        import time
        return f"{max(0, obj.expires_at - time.time()) / 3600:.1f}"
```

## Webhooks

Ver [Webhooks](webhooks.md) para a view completa e as regras de idempotência e dos 5 segundos.
