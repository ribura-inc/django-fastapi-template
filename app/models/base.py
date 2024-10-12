import uuid
from collections.abc import Iterable

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    ###########################################################################
    # ID系
    # idはデバッグ・ログ用
    id = models.BigAutoField(
        verbose_name=_("ID"),
        primary_key=True,
        editable=False,
    )
    # uidは外部API用（idを使用するとオブジェクトボリュームがバレるため）
    MAX_MODEL_CLASS_NAME_LENGTH = 50
    UID_LENGTH = 8
    uid = models.CharField(
        verbose_name=_("UID"),
        db_index=True,
        unique=True,
        editable=False,
        max_length=MAX_MODEL_CLASS_NAME_LENGTH + UID_LENGTH,
    )

    ###########################################################################
    # Timestamp系
    ###########################################################################
    created_at = models.DateTimeField(
        verbose_name=_("created_at"),
        db_index=True,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated_at"),
        db_index=True,
        auto_now=True,
    )

    class Meta:
        abstract = True

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = "default",  # DEFAULT_DB_ALIAS
        update_fields: Iterable[str] | None = None,
    ) -> None:
        """save時にuidを生成する.

        ※uidはswaggerでデバッグしやすいように、モデル名とuuidの一部を組み合わせて生成する.
        """
        if self._state.adding:
            self.uid = f"{self.__class__.__name__.lower()}-{str(uuid.uuid4())[:self.UID_LENGTH]}"
        super().save(force_insert, force_update, using, update_fields)
