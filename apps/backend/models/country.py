from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class Country(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Country"), db_index=True)
    native = models.CharField(
        max_length=255,
        verbose_name=_("Native name"),
        db_index=True,
        null=True,
        blank=True,
    )
    phone_code = models.CharField(
        max_length=10,
        verbose_name=_("Phone code"),
        db_index=True,
        null=True,
        blank=True,
    )
    iso2 = models.CharField(
        max_length=4, verbose_name=_("ISO 2"), db_index=True, null=True, blank=True
    )
    iso3 = models.CharField(
        max_length=4, verbose_name=_("ISO 3"), db_index=True, null=True, blank=True
    )
    emoji = models.CharField(
        max_length=255, verbose_name=_("Emoji"), db_index=True, null=True, blank=True
    )
    emojiU = models.CharField(
        max_length=255, verbose_name=_("EmojiU"), db_index=True, null=True, blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        db_table = "countries"
        ordering = ["name"]

    def __str__(self):
        return self.name
