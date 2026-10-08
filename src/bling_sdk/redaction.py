"""Secret redaction for log records and exception messages.

Tokens, client secrets and Basic credentials must never reach a log file or a traceback.
JWTs are 1500-3000 characters, so a careless debug dump both leaks a credential and
drowns the log.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

MASCARA = "***"

#: Header names whose value is always redacted, lower-cased for comparison.
CABECALHOS_SENSIVEIS = frozenset(
    {"authorization", "proxy-authorization", "cookie", "set-cookie", "x-bling-signature-256"}
)

#: Keys inside JSON bodies and dicts whose value is always redacted.
CHAVES_SENSIVEIS = frozenset(
    {
        "access_token",
        "refresh_token",
        "client_secret",
        "client_id",
        "code",
        "token",
        "password",
        "senha",
        "authorization",
    }
)

#: Bearer tokens and Basic credentials appearing loose in free text.
_PADROES = (
    re.compile(r"(Bearer\s+)[\w\-.=+/]{8,}", re.IGNORECASE),
    re.compile(r"(Basic\s+)[\w\-.=+/]{8,}", re.IGNORECASE),
    # JWTs: three base64url segments. Caught even without a Bearer prefix.
    re.compile(r"()\beyJ[\w-]{4,}\.[\w-]{4,}\.[\w-]{4,}\b"),
)


def redigir_texto(texto: str) -> str:
    """Mask credentials in free text, e.g. an error body echoed back by the server."""
    for padrao in _PADROES:
        texto = padrao.sub(lambda m: f"{m.group(1)}{MASCARA}", texto)
    return texto


def redigir_cabecalhos(cabecalhos: Mapping[str, str]) -> dict[str, str]:
    return {
        k: (MASCARA if k.lower() in CABECALHOS_SENSIVEIS else v) for k, v in cabecalhos.items()
    }


def redigir(valor: Any) -> Any:
    """Recursively mask sensitive values in dicts, lists and strings."""
    if isinstance(valor, Mapping):
        return {
            k: (MASCARA if str(k).lower() in CHAVES_SENSIVEIS else redigir(v))
            for k, v in valor.items()
        }
    if isinstance(valor, (list, tuple)):
        return [redigir(v) for v in valor]
    if isinstance(valor, str):
        return redigir_texto(valor)
    return valor
