"""Token stores.

``JSONFileTokenStore`` is the default and is what scripts and cron jobs should use. Tokens
never live next to the code, never inside ``site-packages``, and never in a plain ``.txt``
alongside the package -- all three were real problems in the integration this replaces.
"""

from __future__ import annotations

import json
import threading
from collections.abc import Callable
from pathlib import Path

from .._filelock import escrever_atomico, trava
from ..config import caminho_tokens_padrao
from ..errors import BlingError
from .tokens import Token

VERSAO_ARQUIVO = 1


class InMemoryTokenStore:
    """Process-local storage. Fine for tests and one-shot scripts; nothing is persisted."""

    def __init__(self) -> None:
        self._dados: dict[str, Token] = {}
        self._lock = threading.Lock()

    def get(self, empresa: str) -> Token | None:
        with self._lock:
            return self._dados.get(empresa)

    def set(self, empresa: str, token: Token) -> None:
        with self._lock:
            self._dados[empresa] = token

    def atualizar(self, empresa: str, renovar: Callable[[Token | None], Token]) -> Token:
        with self._lock:
            token = renovar(self._dados.get(empresa))
            self._dados[empresa] = token
            return token


class JSONFileTokenStore:
    """One JSON file holding every company's tokens.

    Default location ``~/.config/bling-sdk/tokens.json`` (``BLING_SDK_HOME`` overrides).
    Every read and write happens under a sidecar file lock, and writes go through a temp
    file plus ``os.replace``, so a crash cannot leave a half-written file.

    On Windows ``chmod(0o600)`` only toggles the read-only bit -- NTFS permissions are
    ACL-based. The store does what it can; see docs/auth.md.
    """

    def __init__(self, caminho: Path | str | None = None) -> None:
        self.caminho = Path(caminho) if caminho else caminho_tokens_padrao()

    def _ler(self) -> dict[str, dict[str, object]]:
        if not self.caminho.exists():
            return {}
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8") or "{}")
        except (OSError, ValueError) as exc:
            # Never reset silently: that would discard a 30-day authorization and send the
            # user back through the browser flow with no idea why.
            raise BlingError(
                f"o arquivo de tokens {self.caminho} esta ilegivel ou corrompido ({exc}). "
                "Conserte ou apague o arquivo e rode `bling auth` de novo."
            ) from exc
        if not isinstance(dados, dict):
            raise BlingError(f"o arquivo de tokens {self.caminho} nao contem um objeto JSON.")
        empresas = dados.get("empresas", {})
        return empresas if isinstance(empresas, dict) else {}

    def _escrever(self, empresas: dict[str, dict[str, object]]) -> None:
        conteudo = json.dumps(
            {"versao": VERSAO_ARQUIVO, "empresas": empresas}, indent=2, ensure_ascii=False
        )
        escrever_atomico(self.caminho, conteudo + "\n")

    def get(self, empresa: str) -> Token | None:
        with trava(self.caminho):
            bruto = self._ler().get(empresa)
        return Token.model_validate(bruto) if bruto else None

    def set(self, empresa: str, token: Token) -> None:
        with trava(self.caminho):
            empresas = self._ler()
            empresas[empresa] = token.model_dump(mode="json")
            self._escrever(empresas)

    def atualizar(self, empresa: str, renovar: Callable[[Token | None], Token]) -> Token:
        """Hold the lock across read -> refresh -> write.

        This is what makes concurrent processes safe. Bling rotates the refresh_token on
        use, so without it two workers refreshing at once leave one of them holding a token
        Bling has already invalidated -- and the only cure is re-authorizing by hand.
        """
        with trava(self.caminho, timeout=60.0):
            empresas = self._ler()
            bruto = empresas.get(empresa)
            atual = Token.model_validate(bruto) if bruto else None
            token = renovar(atual)
            empresas[empresa] = token.model_dump(mode="json")
            self._escrever(empresas)
            return token

    def listar(self) -> list[str]:
        with trava(self.caminho):
            return sorted(self._ler())

    def remover(self, empresa: str) -> bool:
        with trava(self.caminho):
            empresas = self._ler()
            if empresa not in empresas:
                return False
            del empresas[empresa]
            self._escrever(empresas)
            return True
