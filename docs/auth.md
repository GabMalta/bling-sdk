# Autenticação

O Bling usa OAuth 2.0 com apenas o grant `authorization_code`.

## O caminho curto

```bash
export BLING_CLIENT_ID=...
export BLING_CLIENT_SECRET=...
bling auth --empresa minha-loja
```

Isso cobre os quatro passos abaixo e grava os tokens em
`~/.config/bling-sdk/tokens.json`. Dali em diante o `BlingClient` renova sozinho.

## O fluxo, passo a passo

### 1. Cadastre o app no painel do Bling

Em **Aplicativos → novo aplicativo**, marque os **escopos** dos recursos que vai usar e
informe a **URL de redirecionamento**.

!!! warning "A URL de redirecionamento é cadastrada, não enviada"
    O Bling **ignora** `redirect_uri` e `scope` enviados na requisição de autorização e usa
    sempre o que está no cadastro do app. Por isso a URL que o `bling auth` escuta
    (`http://127.0.0.1:8080/callback` por padrão) tem de ser exatamente a cadastrada —
    e por isso um `403 insufficient_scope` se resolve no painel, não no código.

### 2. Mande o usuário autorizar

```python
url, state = bling.url_autorizacao()
# guarde `state` na sessão e redirecione o usuário para `url`
```

### 3. Receba o callback e valide o `state`

O Bling redireciona para `...?code=...&state=...`. Compare o `state` recebido com o que você
guardou — é a proteção contra CSRF. Se não bater, interrompa.

### 4. Troque o code pelos tokens

```python
token = bling.trocar_codigo(code)
```

!!! danger "O code expira em 60 segundos"
    Não coloque nada lento entre receber o callback e chamar `trocar_codigo`. Sem fila, sem
    task assíncrona, sem uma consulta pesada no meio.

## Tempos de vida

| | validade |
|---|---|
| authorization code | 1 minuto |
| access token | 6 horas |
| refresh token | 30 dias |

O cliente renova o access token **5 minutos antes** de expirar (`folga_renovacao`), de forma
preguiçosa: nada acontece até você fazer uma chamada.

!!! warning "O refresh token rota a cada uso"
    Cada renovação devolve um refresh token novo e **invalida o anterior**. Se dois processos
    renovarem ao mesmo tempo, um deles fica com um token que o Bling já descartou, e a única
    cura é reautorizar à mão.

    O SDK evita isso em duas camadas: um lock em processo (N threads → **uma** chamada a
    `/oauth/token`) e, para stores que implementam `atualizar()`, um lock entre processos que
    cobre ler → renovar → gravar. O `JSONFileTokenStore` e o `DjangoTokenStore` fazem as
    duas. Um store seu que implemente só `get`/`set` tem apenas a primeira.

Há ainda uma razão dura para não renovar à toa: **20 chamadas a `/oauth/token` em 60
segundos banem o seu IP por 60 minutos**, e o ban derruba todas as empresas de uma vez. Por
isso o endpoint de token tem rate limiter próprio (10/60s) e a renovação nunca acontece na
construção do cliente.

## JWT — migre agora

O Bling **descontinuou o token opaco**. A data de bloqueio ainda não foi anunciada.

Para receber JWT basta o header `enable-jwt: 1`, e ele precisa ser mantido **em toda
requisição autenticada**, não só na de token. O SDK faz isso por padrão
(`enable_jwt=True`). Você não precisa fazer nada.

JWTs têm 1.500 a 3.000 caracteres. Se você guarda tokens num banco, a coluna precisa ser
`TEXT`, não `VARCHAR(255)`.

```python
# só se você precisar do comportamento antigo, por algum motivo
bling = BlingClient(..., enable_jwt=False)
```

Se você já tem um token opaco gravado e liga o JWT, o SDK emite um `WARNING` uma vez e a
próxima renovação promove o token.

## Onde os tokens ficam

```python
from bling_sdk import JSONFileTokenStore, InMemoryTokenStore

# padrao: ~/.config/bling-sdk/tokens.json, com lock de arquivo e escrita atomica
BlingClient(..., token_store=JSONFileTokenStore())

# caminho proprio
BlingClient(..., token_store=JSONFileTokenStore("/var/lib/app/bling.json"))

# so em memoria (testes, scripts de uma vez)
BlingClient(..., token_store=InMemoryTokenStore())
```

`BLING_SDK_HOME` muda o diretório base.

O arquivo é escrito com modo `0600` e o diretório com `0700`, na medida do possível. **No
Windows isso é só o bit de somente-leitura** — permissões NTFS são ACL e `os.chmod` não as
toca. Se o arquivo precisa de proteção real ali, use ACL ou um store próprio.

Um arquivo de tokens corrompido levanta erro apontando o caminho; o store **nunca** reseta em
silêncio, porque isso jogaria fora uma autorização de 30 dias.

### Store próprio

```python
from bling_sdk import Token

class MeuStore:
    def get(self, empresa: str) -> Token | None: ...
    def set(self, empresa: str, token: Token) -> None: ...

    # opcional, mas recomendado: habilita deduplicacao entre processos
    def atualizar(self, empresa, renovar):
        with meu_lock(empresa):
            atual = self.get(empresa)
            novo = renovar(atual)
            self.set(empresa, novo)
            return novo
```

Para Django existe adapter pronto — ver [Django](django.md).

## Revogação

```python
bling.revogar()                      # so o refresh token desta empresa
bling.revogar(tipo="access_token")   # so o access token
```

!!! danger "Revogação ampliada é irreversível"
    `acao="uninstall"` e `alvo="company"` revogam **todos** os tokens do usuário ou da
    empresa. Todo mundo afetado precisa passar pelo navegador de novo. O SDK nunca usa esses
    parâmetros por conta própria.

## Diagnóstico

```bash
bling info --empresa minha-loja     # validade, escopos, flag jwt -- nunca o token
bling empresa --empresa minha-loja  # o companyId que chega nos webhooks
```

`repr(Token)` é redigido de propósito: um JWT é credencial viva e não pode aparecer em
traceback, log ou diff de teste.
