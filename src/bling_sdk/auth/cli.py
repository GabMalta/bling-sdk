"""The ``bling`` command line tool.

``bling auth`` runs the whole three-legged OAuth dance: it starts a one-shot local HTTP
server, opens the browser, captures the ``?code=``, exchanges it and persists the tokens.

That replaces the ``input()`` prompt and the Django management command the previous
integration needed, and it is why ``BlingClient`` never has to prompt for anything.

Standard library only: argparse, http.server, webbrowser, secrets, hmac.
"""

from __future__ import annotations

import argparse
import hmac
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from ..config import caminho_tokens_padrao
from ..errors import BlingError, BlingSemToken
from .oauth import gerar_state
from .stores import JSONFileTokenStore

PAGINA_OK = b"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Autorizado</title><style>
body{font-family:system-ui,sans-serif;display:grid;place-items:center;height:100vh;margin:0;
background:#f6f7f9;color:#1b1f24}div{text-align:center}h1{font-size:1.25rem;margin:0 0 .5rem}
p{margin:0;color:#57606a}</style></head><body><div>
<h1>Pronto</h1><p>Tokens gravados. Voce pode fechar esta aba.</p>
</div></body></html>"""

PAGINA_ERRO = b"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Falhou</title><style>
body{font-family:system-ui,sans-serif;display:grid;place-items:center;height:100vh;margin:0;
background:#f6f7f9;color:#1b1f24}div{text-align:center}h1{font-size:1.25rem;margin:0 0 .5rem}
p{margin:0;color:#57606a}</style></head><body><div>
<h1>Autorizacao nao concluida</h1><p>Volte ao terminal para ver o motivo.</p>
</div></body></html>"""


class _Captura:
    """Shared slot for whatever the callback receives."""

    def __init__(self) -> None:
        self.code: str | None = None
        self.state: str | None = None
        self.erro: str | None = None
        self.pronto = threading.Event()


def _handler(captura: _Captura, path_esperado: str) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - nome exigido por BaseHTTPRequestHandler
            partes = urlparse(self.path)
            if partes.path != path_esperado:
                self.send_response(404)
                self.end_headers()
                return
            q = parse_qs(partes.query)
            def primeiro(chave: str) -> str | None:
                valores = q.get(chave)
                return valores[0] if valores else None

            captura.code = primeiro("code")
            captura.state = primeiro("state")
            captura.erro = primeiro("error")
            corpo = PAGINA_OK if captura.code else PAGINA_ERRO
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)
            captura.pronto.set()

        def log_message(self, *args: Any) -> None:
            """Silence the default stderr access log."""

    return Handler


def _credenciais(args: argparse.Namespace) -> tuple[str, str]:
    client_id = args.client_id or os.getenv("BLING_CLIENT_ID")
    client_secret = args.client_secret or os.getenv("BLING_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise SystemExit(
            "informe --client-id e --client-secret, ou defina BLING_CLIENT_ID e "
            "BLING_CLIENT_SECRET no ambiente. O SDK nunca le credencial de codigo."
        )
    return client_id, client_secret


def _cliente(args: argparse.Namespace) -> Any:
    from ..client import BlingClient

    client_id, client_secret = _credenciais(args)
    store = JSONFileTokenStore(args.tokens) if args.tokens else JSONFileTokenStore()
    return BlingClient(
        client_id,
        client_secret,
        empresa=args.empresa,
        token_store=store,
        enable_jwt=not getattr(args, "no_jwt", False),
    )


def cmd_auth(args: argparse.Namespace) -> int:
    cliente = _cliente(args)
    captura = _Captura()
    state_enviado = gerar_state()
    callback = f"http://{args.host}:{args.porta}{args.path}"

    servidor = ThreadingHTTPServer((args.host, args.porta), _handler(captura, args.path))
    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()

    url, _ = cliente.url_autorizacao(state_enviado)
    print(f"Empresa:  {args.empresa}")
    print(f"Callback: {callback}")
    print(
        "          Essa URL tem de ser EXATAMENTE a 'URL de redirecionamento' cadastrada\n"
        "          no seu app no painel do Bling -- o Bling ignora redirect_uri enviado\n"
        "          na requisicao e usa sempre o que esta cadastrado."
    )
    print(f"\nAbra para autorizar:\n  {url}\n")
    if not args.no_browser:
        webbrowser.open(url)

    try:
        if not captura.pronto.wait(timeout=args.timeout):
            print(f"nada chegou no callback em {args.timeout}s; abortando.", file=sys.stderr)
            return 3
    finally:
        servidor.shutdown()
        servidor.server_close()

    if captura.erro or not captura.code:
        print(f"autorizacao negada pelo Bling: {captura.erro or 'sem code'}", file=sys.stderr)
        return 1
    # `state` protege contra CSRF; comparacao em tempo constante por higiene.
    if not captura.state or not hmac.compare_digest(captura.state, state_enviado):
        print("o state retornado nao corresponde ao enviado; fluxo interrompido.",
              file=sys.stderr)
        return 1

    try:
        # O code expira em 60 SEGUNDOS, entao a troca vem imediatamente depois da captura.
        token = cliente.trocar_codigo(captura.code)
    except BlingError as exc:
        print(f"falha ao trocar o code pelos tokens: {exc}", file=sys.stderr)
        return 2
    finally:
        cliente.close()

    print(f"OK. Tokens gravados para a empresa {args.empresa!r}.")
    print(f"  access_token expira em ~{token.segundos_restantes() / 3600:.1f}h")
    print("  refresh_token vale 30 dias")
    print(f"  escopos autorizados: {len(token.escopos())}")
    print(f"  jwt: {token.jwt}")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    store = JSONFileTokenStore(args.tokens) if args.tokens else JSONFileTokenStore()
    empresas = store.listar()
    if not empresas:
        print(f"nenhum token em {store.caminho}. Rode `bling auth`.", file=sys.stderr)
        return 1
    alvos = [args.empresa] if args.empresa else empresas
    print(f"arquivo: {store.caminho}\n")
    for empresa in alvos:
        token = store.get(empresa)
        if token is None:
            print(f"{empresa}: sem token", file=sys.stderr)
            continue
        estado = "EXPIRADO" if token.expirado() else f"{token.segundos_restantes() / 3600:.1f}h"
        # Nunca imprimimos o token em si.
        print(f"{empresa}:")
        print(f"  access_token: expira em {estado}")
        print(f"  jwt:          {token.jwt}")
        print(f"  escopos:      {len(token.escopos())} ({' '.join(token.escopos()[:5])}...)")
    return 0


def cmd_revoke(args: argparse.Namespace) -> int:
    cliente = _cliente(args)
    try:
        cliente.revogar(tipo=args.tipo, acao=args.action, alvo=args.target)
    except (BlingError, BlingSemToken) as exc:
        print(f"falha ao revogar: {exc}", file=sys.stderr)
        return 2
    finally:
        cliente.close()
    print(f"token revogado para {args.empresa!r} (tipo={args.tipo}).")
    return 0


def cmd_empresa(args: argparse.Namespace) -> int:
    cliente = _cliente(args)
    try:
        dados = cliente.dados_empresa()
    except BlingError as exc:
        print(f"falha ao consultar a empresa: {exc}", file=sys.stderr)
        return 2
    finally:
        cliente.close()
    import json

    print(json.dumps(dados, indent=2, ensure_ascii=False))
    return 0


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bling", description="Autorizacao e diagnostico do Bling v3.")
    sub = p.add_subparsers(dest="comando", required=True)

    def comuns(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--empresa", default="default", help="apelido da conta Bling")
        sp.add_argument("--tokens", default=None,
                        help=f"arquivo de tokens (padrao: {caminho_tokens_padrao()})")
        sp.add_argument("--client-id", default=None, help="ou BLING_CLIENT_ID")
        sp.add_argument("--client-secret", default=None, help="ou BLING_CLIENT_SECRET")

    a = sub.add_parser("auth", help="autoriza o app e grava os tokens")
    comuns(a)
    a.add_argument("--host", default="127.0.0.1")
    a.add_argument("--porta", type=int, default=8080)
    a.add_argument("--path", default="/callback")
    a.add_argument("--no-jwt", action="store_true",
                   help="emite token opaco (descontinuado pelo Bling)")
    a.add_argument("--no-browser", action="store_true")
    a.add_argument("--timeout", type=float, default=300.0)
    a.set_defaults(func=cmd_auth)

    i = sub.add_parser("info", help="mostra validade e escopos, nunca o token")
    i.add_argument("--empresa", default=None)
    i.add_argument("--tokens", default=None)
    i.set_defaults(func=cmd_info)

    r = sub.add_parser("revoke", help="revoga um token")
    comuns(r)
    r.add_argument("--tipo", choices=["access_token", "refresh_token"], default="refresh_token")
    r.add_argument("--action", choices=["logout", "uninstall"], default=None,
                   help="AMPLIA a revogacao; irreversivel")
    r.add_argument("--target", choices=["user", "company"], default=None,
                   help="AMPLIA a revogacao; irreversivel")
    r.set_defaults(func=cmd_revoke)

    e = sub.add_parser("empresa", help="GET /empresas/me/dados-basicos (mostra o companyId)")
    comuns(e)
    e.set_defaults(func=cmd_empresa)

    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    resultado: int = args.func(args)
    return resultado


if __name__ == "__main__":
    raise SystemExit(main())
