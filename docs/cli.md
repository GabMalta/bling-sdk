# CLI

Instalado junto com o pacote, como `bling`.

## `bling auth`

Roda o OAuth inteiro: sobe um servidor local, abre o navegador, captura o `?code=`, troca e
grava os tokens.

```bash
export BLING_CLIENT_ID=...
export BLING_CLIENT_SECRET=...
bling auth --empresa minha-loja
```

```
Empresa:  minha-loja
Callback: http://127.0.0.1:8080/callback
          Essa URL tem de ser EXATAMENTE a 'URL de redirecionamento' cadastrada
          no seu app no painel do Bling -- o Bling ignora redirect_uri enviado
          na requisicao e usa sempre o que esta cadastrado.

Abra para autorizar:
  https://www.bling.com.br/Api/v3/oauth/authorize?response_type=code&client_id=...

OK. Tokens gravados para a empresa 'minha-loja'.
  access_token expira em ~6.0h
  refresh_token vale 30 dias
  escopos autorizados: 14
  jwt: True
```

| opção | padrão | |
|---|---|---|
| `--empresa` | `default` | apelido da conta |
| `--host` / `--porta` / `--path` | `127.0.0.1` / `8080` / `/callback` | tem de bater com o cadastro |
| `--client-id` / `--client-secret` | `$BLING_CLIENT_ID` / `$BLING_CLIENT_SECRET` | |
| `--tokens` | `~/.config/bling-sdk/tokens.json` | |
| `--no-browser` | | só imprime a URL |
| `--no-jwt` | | emite token opaco (descontinuado) |
| `--timeout` | `300` | espera pelo callback |

Códigos de saída: `0` ok, `1` negado ou `state` divergente, `2` falha na troca, `3` timeout.

O `state` é gerado por chamada e comparado em tempo constante. A troca do code acontece
imediatamente depois da captura, porque o code expira em **60 segundos**.

## `bling info`

```bash
bling info                       # todas as empresas
bling info --empresa minha-loja
```

Mostra validade, flag JWT e quantidade de escopos. **Nunca imprime o token.**

## `bling empresa`

```bash
bling empresa --empresa minha-loja
```

`GET /empresas/me/dados-basicos`. É como você descobre o `companyId` que chega nos webhooks —
ver [Multi-empresa](multi-empresa.md).

## `bling revoke`

```bash
bling revoke --empresa minha-loja                      # só o refresh token
bling revoke --empresa minha-loja --tipo access_token
```

!!! danger "`--action` e `--target` ampliam a revogação e são irreversíveis"
    `--action uninstall --target company` revoga **todos** os tokens da empresa. Todo usuário
    afetado precisa reautorizar pelo navegador.
