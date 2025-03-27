from django.db.models import (
    BigIntegerField,
    BooleanField,
    CharField,
    TextChoices,
)
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class RoleChoices(TextChoices):
    ADMIN = "admin", _("Admin")
    MODERATOR = "moderator", _("Moderator")
    USER = "user", _("User")


class LanguageChoices(TextChoices):
    UZ = "uz", _("Uzbek")
    RU = "ru", _("Russian")
    EN = "en", _("English")


class BotUser(AbstractBaseModel):
    telegram_id = BigIntegerField(unique=True, verbose_name=_("Telegram ID"))
    username = CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Username"),
    )
    first_name = CharField(
        max_length=255, null=True, blank=True, verbose_name=_("First Name")
    )
    last_name = CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Last Name")
    )
    full_name = CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Full Name")
    )
    phone = BigIntegerField(
        null=True, blank=True, unique=True, verbose_name=_("Phone Number")
    )
    language_code = CharField(
        max_length=10,
        choices=LanguageChoices,
        default=LanguageChoices.UZ,
        verbose_name=_("Language"),
    )
    is_active = BooleanField(default=True, verbose_name=_("Is Active"))
    role = CharField(
        max_length=10,
        choices=RoleChoices,
        default=RoleChoices.USER,
        verbose_name=_("Role"),
    )

    class Meta:
        db_table = "bot_user"
        verbose_name = _("Bot User")
        verbose_name_plural = _("Bot Users")
        ordering = ["-created_at"]

    def __str__(self):
        return f"ID: {self.id} - {self.telegram_id}"
