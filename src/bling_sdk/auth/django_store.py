"""Optional Django ORM token store.

This module is **never** imported by the package itself, and Django is imported inside the
methods, so ``bling_sdk`` stays importable without Django installed.

It exists so a Django project can drop its own hand-rolled Bling client and keep storing
tokens in the database it already has.

Wiring:

    # minhaapp/models.py
    from bling_sdk.auth.django_store import BlingTokenBase

    class BlingToken(BlingTokenBase):
        pass

    # onde o cliente e criado
    from bling_sdk import BlingClient
    from bling_sdk.auth.django_store import DjangoTokenStore
    from minhaapp.models import BlingToken

    bling = BlingClient(
        settings.BLING_CLIENT_ID,
        settings.BLING_CLIENT_SECRET,
        empresa="legitima",
        token_store=DjangoTokenStore(BlingToken),
    )

``DjangoTokenStore`` implements ``atualizar()``, so refreshes are de-duplicated across
processes via ``select_for_update()``. That matters because Bling rotates the refresh token
on every use: two gunicorn workers refreshing concurrently would leave one holding a token
Bling has already invalidated.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from .tokens import Token

if TYPE_CHECKING:  # pragma: no cover
    from django.db.models import Model


def _modelo_base() -> Any:
    """Build the abstract model lazily, so importing this file never needs Django."""
    from django.db import models

    class BlingTokenBase(models.Model):
        """Abstract model holding one Bling token pair per company.

        Subclass it in your own app and run ``makemigrations``. JWTs reach 3000 characters,
        so the token columns are ``TextField`` rather than ``CharField``.
        """

        empresa = models.CharField(max_length=100, unique=True, db_index=True)
        access_token = models.TextField()
        refresh_token = models.TextField()
        expires_at = models.FloatField(help_text="Unix epoch em segundos")
        token_type = models.CharField(max_length=20, default="Bearer")
        scope = models.TextField(blank=True, default="")
        jwt = models.BooleanField(default=False)
        obtido_em = models.FloatField(default=0.0)
        atualizado_em = models.DateTimeField(auto_now=True)

        class Meta:
            abstract = True
            verbose_name = "token do Bling"
            verbose_name_plural = "tokens do Bling"

        def __str__(self) -> str:
            return f"BlingToken({self.empresa})"

    return BlingTokenBase


def __getattr__(nome: str) -> Any:
    """Expose ``BlingTokenBase`` without importing Django at module load."""
    if nome == "BlingTokenBase":
        return _modelo_base()
    raise AttributeError(nome)


CAMPOS = (
    "access_token",
    "refresh_token",
    "expires_at",
    "token_type",
    "scope",
    "jwt",
    "obtido_em",
)


class DjangoTokenStore:
    """A :class:`~bling_sdk.auth.TokenStore` backed by a Django model.

    ``modelo`` is your concrete subclass of ``BlingTokenBase``, or any model carrying the
    same field names.
    """

    def __init__(self, modelo: type[Model], campo_empresa: str = "empresa") -> None:
        self.modelo = modelo
        self.campo_empresa = campo_empresa

    def _para_token(self, linha: Any) -> Token:
        return Token(**{campo: getattr(linha, campo) for campo in CAMPOS})

    def get(self, empresa: str) -> Token | None:
        linha = self.modelo.objects.filter(**{self.campo_empresa: empresa}).first()
        return self._para_token(linha) if linha else None

    def set(self, empresa: str, token: Token) -> None:
        self.modelo.objects.update_or_create(
            **{self.campo_empresa: empresa},
            defaults={campo: getattr(token, campo) for campo in CAMPOS},
        )

    def atualizar(self, empresa: str, renovar: Callable[[Token | None], Token]) -> Token:
        """Hold a row lock across read -> refresh -> write.

        ``select_for_update()`` makes concurrent processes queue instead of racing, which is
        what protects the rotating refresh token. Requires a backend with row locking
        (PostgreSQL, MySQL); on SQLite Django ignores it and you fall back to the
        in-process lock only.
        """
        from django.db import transaction

        with transaction.atomic():
            linha = (
                self.modelo.objects.select_for_update()
                .filter(**{self.campo_empresa: empresa})
                .first()
            )
            atual = self._para_token(linha) if linha else None
            token = renovar(atual)
            if linha is None:
                self.modelo.objects.create(
                    **{self.campo_empresa: empresa},
                    **{campo: getattr(token, campo) for campo in CAMPOS},
                )
            else:
                for campo in CAMPOS:
                    setattr(linha, campo, getattr(token, campo))
                linha.save(update_fields=[*CAMPOS])
            return token
