"""``/empresas`` -- the authenticated account's own data."""

from __future__ import annotations

from typing import Any

from ._base import Recurso


class Empresas(Recurso):
    """``/empresas``."""

    prefixo = "empresas"

    def dados_basicos(self) -> Any:
        """GET /empresas/me/dados-basicos -> dict.

        Cheap, and the way to discover the ``companyId`` that webhooks arrive under -- which
        is what makes multi-company routing work: keep a ``{companyId: empresa}`` map and
        pass the matching ``empresa=`` to :class:`~bling_sdk.BlingClient`.
        """
        return self._get(self._path("me", "dados-basicos"))
