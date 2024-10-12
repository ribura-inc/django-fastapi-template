from collections.abc import Iterable

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self,
        username: str,
        password: str,
        **extra_fields: dict,
    ) -> "User":
        if not username:
            msg = "The given username must be set."
            raise ValueError(msg)

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, password: str, **extra_fields: dict) -> "User":
        extra_fields.setdefault("is_staff", False)  # type: ignore
        extra_fields.setdefault("is_superuser", False)  # type: ignore
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username: str, password: str, **extra_fields: dict) -> "User":
        extra_fields.setdefault("is_staff", True)  # type: ignore
        extra_fields.setdefault("is_superuser", True)  # type: ignore

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    objects = UserManager()

    MIN_LENGTH_USERNAME = 3
    MAX_LENGTH_USERNAME = 20
    username = models.CharField(
        "username",
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
    )
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)

    ###########################################################################
    # permissions
    ###########################################################################
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = "default",  # DEFAULT_DB_ALIAS
        update_fields: Iterable[str] | None = None,
    ) -> None:
        self.username = self.username.lower()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return self.username
