"""Webhook signature verification and event parsing.

Three things this module must get right, each covered by a test:

1. the HMAC key is the app's **client_secret**, and the message is the **raw request
   bytes**. The API therefore takes ``bytes``, never a dict -- re-serializing JSON changes
   key order and whitespace, and therefore the digest;
2. comparison uses :func:`hmac.compare_digest`, and accepts both ``sha256=<hex>`` and a
   bare ``<hex>``;
3. verification happens **before** the body is parsed as JSON.

Operational notes that belong in your handler, not here:

* answer **2xx within 5 seconds** or Bling retries. Enqueue, never process inline.
* delivery is **unordered** and **duplicated** -- an ``updated`` can arrive before the
  ``created`` for the same record. Key idempotency on ``event_id``.
* moving a record's ``situacao`` to excluded emits ``updated``, not ``deleted``.
* after 3 days of failures Bling **disables** the webhook config, and only a human can
  re-enable it in the panel.
"""

from __future__ import annotations

import hashlib
import hmac

from .config import CABECALHO_ASSINATURA
from .errors import BlingAssinaturaInvalida
from .models.webhooks import EventoWebhook

__all__ = [
    "ACOES",
    "CABECALHO_ASSINATURA",
    "RECURSOS",
    "EventoWebhook",
    "assinar",
    "exigir_assinatura",
    "parse_evento",
    "verificar_assinatura",
]

#: Webhook resources, which double as the scope names to tick on the app in the panel.
RECURSOS = frozenset(
    {
        "order",
        "product",
        "stock",
        "virtual_stock",
        "product_supplier",
        "invoice",
        "consumer_invoice",
    }
)

ACOES = frozenset({"created", "updated", "deleted"})

_PREFIXO = "sha256="


def assinar(corpo: bytes, client_secret: str) -> str:
    """The hex HMAC-SHA256 digest Bling would send for this body, without the prefix."""
    return hmac.new(client_secret.encode("utf-8"), corpo, hashlib.sha256).hexdigest()


def verificar_assinatura(corpo: bytes, assinatura: str | None, client_secret: str) -> bool:
    """Whether ``assinatura`` matches ``corpo``.

    ``corpo`` must be the exact bytes received. Reading the request as a dict and dumping it
    again will not produce the same digest.
    """
    if not assinatura:
        return False
    recebida = assinatura.strip()
    if recebida.lower().startswith(_PREFIXO):
        recebida = recebida[len(_PREFIXO) :]
    return hmac.compare_digest(recebida.lower(), assinar(corpo, client_secret).lower())


def exigir_assinatura(corpo: bytes, assinatura: str | None, client_secret: str) -> None:
    """Raise :class:`~bling_sdk.errors.BlingAssinaturaInvalida` unless the HMAC matches."""
    if not verificar_assinatura(corpo, assinatura, client_secret):
        raise BlingAssinaturaInvalida(
            f"o header {CABECALHO_ASSINATURA} nao corresponde ao HMAC-SHA256 do corpo "
            "recebido. Confira se voce esta usando o client_secret do app e os BYTES crus "
            "da request (nao o JSON re-serializado)."
        )


def parse_evento(
    corpo: bytes,
    *,
    assinatura: str | None = None,
    client_secret: str | None = None,
) -> EventoWebhook:
    """Verify (when a secret is given) and parse a webhook body.

    Pass both ``assinatura`` and ``client_secret`` in production. Verification runs before
    any JSON parsing, so a forged body is rejected without being interpreted.
    """
    if client_secret is not None:
        exigir_assinatura(corpo, assinatura, client_secret)
    return EventoWebhook.model_validate_json(corpo)
