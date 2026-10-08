# Limites e retry

## Os limites do Bling

Por **conta Bling** — não por app, não por token — somando todos os endpoints:

| limite | valor |
|---|---|
| requisições por segundo | 3 |
| requisições por dia | 120.000 |

E bloqueios de IP, que são o risco maior:

| gatilho | duração do bloqueio |
|---|---|
| 300 erros em 10 s | 10 min |
| 600 requisições em 10 s | 10 min |
| 20 requisições a `/oauth/token` em 60 s | **60 min** |

Reincidência pode levar a bloqueio por tempo indeterminado. É por isso que o SDK prefere
esperar a tomar 429: um 429 custa um erro na cota de bloqueio por IP.

## O rate limiter

Por padrão, uma janela deslizante em processo, por empresa:

```python
bling = BlingClient(...)   # ja vem com limitador_padrao(empresa)
```

São duas restrições combinadas, porque nenhuma sozinha basta:

- **janela deslizante** — espaçar em intervalos fixos de `periodo / max_chamadas` deixaria 4
  chamadas caberem em 1 segundo (instantes 0, ⅓, ⅔ e 1.0);
- **intervalo mínimo** — só a janela deslizante libera 3 chamadas no mesmo milissegundo
  quando a fila está vazia, e a rajada chega ao servidor junta.

Ao tomar um 429, `penalize()` pausa **todas** as threads. Desacelerar só a thread que levou o
429 não resolve nada: as outras seguem no mesmo ritmo.

A janela é alargada em 5% (`margem`) porque o relógio que conta é o do servidor, e jitter de
agendamento e de rede basta para a chamada seguinte cair dentro da janela dele.

### Mais de um processo na mesma conta

O limiter em processo não vê os outros processos. Um cron job e um worker web na mesma conta
Bling passam de 3 req/s juntos e ganham um bloqueio de IP. Para esse caso:

```python
from bling_sdk import ArquivoRateLimiter

bling = BlingClient(..., rate_limiter=ArquivoRateLimiter(empresa="minha-loja"))
```

O estado vira um JSON pequeno sob lock de arquivo, compartilhado entre processos. Usa
`time.time()` e não `time.monotonic()`, porque relógio monotônico não é comparável entre
processos — o preço é sensibilidade a saltos de relógio (NTP), irrelevante a 3 req/s.

### Mais de uma conta

```python
loja_a = BlingClient(..., empresa="loja-a")
loja_b = BlingClient(..., empresa="loja-b")
```

Cada empresa ganha seu próprio limiter: o orçamento é por conta, então compartilhar um
limiter entre duas contas cortaria a vazão pela metade. Dois `BlingClient` da **mesma**
empresa compartilham o mesmo limiter automaticamente.

`BLING_SDK_RATE_LIMIT` muda a taxa, se algum dia o Bling liberar mais para o seu app.

### Limiter próprio

```python
from bling_sdk import registrar_limitador, SemLimite

registrar_limitador("minha-loja", SemLimite())        # testes
registrar_limitador("minha-loja", MeuLimiterRedis())  # qualquer coisa com acquire/penalize
```

## A política de retry

A regra que mais importa neste SDK:

!!! danger "GET/PUT/PATCH/DELETE repetem. POST repete só em 429."
    Um 429 é recusado **antes** do processamento, então a requisição comprovadamente não teve
    efeito — repetir é seguro para qualquer verbo.

    Já um 5xx ou um timeout num `POST /estoques` pode significar que o Bling **lançou** o
    movimento e só a resposta se perdeu. Repetir lançaria o movimento duas vezes, inflando um
    saldo de um jeito que ninguém percebe por semanas.

| situação | GET/PUT/PATCH/DELETE | POST |
|---|---|---|
| 429 `period: second` | repete | repete |
| 429 `period: day` | **falha rápido** | **falha rápido** |
| 5xx | repete | **não repete** |
| erro de rede / timeout | repete | **não repete** |
| 4xx de validação | não repete | não repete |
| 401 | uma renovação forçada, depois desiste | idem |

O 429 diário levanta `BlingLimiteDiario` na primeira resposta. Esperar não ajuda: a cota só
volta amanhã, e estacionar threads por horas é pior do que falhar e deixar você reagendar.

```python
from bling_sdk import BlingLimiteDiario

try:
    bling.produtos.listar()
except BlingLimiteDiario:
    reagendar_para_amanha()
```

### Espera entre tentativas

Honra `Retry-After` quando o Bling manda; senão backoff exponencial (2, 4, 8, 16s) com teto
de 30s. Nunca dorme depois da última tentativa.

```python
BlingClient(..., max_tentativas=4, teto_backoff=30.0)
```

### Sobrescrevendo por chamada

```python
# uma acao que voce sabe ser segura repetir
bling.request("POST", "produtos/variacoes/atributos/gerar-combinacoes",
              json=..., idempotente=True)

# um GET que voce NAO quer ver repetido
bling.request("GET", "relatorio/caro", idempotente=False)
```

## Por que não o retry do httpx

O cliente é criado com `httpx.HTTPTransport(retries=0)` de propósito. Um retry dentro do
transport roda **abaixo** do rate limiter e da política por verbo: não consome slot, logo
amplifica o estouro de limite, e reenviaria um POST sem saber que não devia.

## Filtros de data

Intervalos acima de um ano o Bling recusa com 400. O SDK valida antes de gastar a requisição:

```python
from bling_sdk import BlingIntervaloInvalido, fatiar_periodo

try:
    bling.pedidos.vendas.listar(data_inicial="2020-01-01", data_final="2026-01-01")
except BlingIntervaloInvalido as e:
    print(e)   # sugere fatiar_periodo

# o jeito certo
for inicio, fim in fatiar_periodo(date(2020, 1, 1), date(2026, 1, 1)):
    pedidos = bling.pedidos.vendas.listar(data_inicial=inicio, data_final=fim)
```

A validação é automática; o fatiamento é explícito de propósito — transformar uma chamada em
quatorze em silêncio é o tipo de surpresa que queima a cota diária.

## Bloqueio de IP

A resposta de um bloqueio quase certamente não é o envelope JSON da API (vem do edge/WAF).
Nesse caso o SDK levanta `BlingErroTransporte` com um trecho redigido do corpo, em vez de
estourar com erro de parsing. Isso **não foi testado contra a API real** — testar exigiria
provocar um bloqueio.
