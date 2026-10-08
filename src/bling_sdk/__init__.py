"""SDK Python para a API v3 do Bling ERP.

    from bling_sdk import BlingClient

    with BlingClient(client_id="...", client_secret="...", empresa="minha-loja") as bling:
        for produto in bling.produtos.iter_todos():
            print(produto.id, produto.nome, produto.preco)

Autorize uma vez com ``bling auth --empresa minha-loja``.
"""

from .auth import (
    InMemoryTokenStore,
    JSONFileTokenStore,
    Token,
    TokenStore,
    TokenStoreTransacional,
    gerar_state,
)
from .client import BlingClient
from .config import (
    API_BASE,
    LIMITE_PADRAO,
    REQUISICOES_POR_DIA,
    REQUISICOES_POR_SEGUNDO,
    __version__,
)
from .errors import (
    BlingAssinaturaInvalida,
    BlingErroAPI,
    BlingError,
    BlingErroServidor,
    BlingErroTransporte,
    BlingErroValidacao,
    BlingIntervaloInvalido,
    BlingLimiteDiario,
    BlingLimiteExcedido,
    BlingLimitePorSegundo,
    BlingNaoAutenticado,
    BlingNaoEncontrado,
    BlingSemPermissao,
    BlingSemToken,
    BlingSubstituicaoNaoConfirmada,
)
from .pagination import fatiar_periodo, iter_paginas
from .ratelimit import (
    ArquivoRateLimiter,
    JanelaDeslizanteRateLimiter,
    RateLimiter,
    SemLimite,
    limitador_padrao,
    registrar_limitador,
)
from .webhooks import (
    EventoWebhook,
    assinar,
    exigir_assinatura,
    parse_evento,
    verificar_assinatura,
)

__all__ = [
    "API_BASE",
    "LIMITE_PADRAO",
    "REQUISICOES_POR_DIA",
    "REQUISICOES_POR_SEGUNDO",
    "ArquivoRateLimiter",
    "BlingAssinaturaInvalida",
    "BlingClient",
    "BlingErroAPI",
    "BlingErroServidor",
    "BlingErroTransporte",
    "BlingErroValidacao",
    "BlingError",
    "BlingIntervaloInvalido",
    "BlingLimiteDiario",
    "BlingLimiteExcedido",
    "BlingLimitePorSegundo",
    "BlingNaoAutenticado",
    "BlingNaoEncontrado",
    "BlingSemPermissao",
    "BlingSemToken",
    "BlingSubstituicaoNaoConfirmada",
    "EventoWebhook",
    "InMemoryTokenStore",
    "JSONFileTokenStore",
    "JanelaDeslizanteRateLimiter",
    "RateLimiter",
    "SemLimite",
    "Token",
    "TokenStore",
    "TokenStoreTransacional",
    "__version__",
    "assinar",
    "exigir_assinatura",
    "fatiar_periodo",
    "gerar_state",
    "iter_paginas",
    "limitador_padrao",
    "parse_evento",
    "registrar_limitador",
    "verificar_assinatura",
]
