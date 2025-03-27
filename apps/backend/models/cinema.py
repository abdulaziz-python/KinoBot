import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


def validate_telegram_message_url(value):
    pattern = r"^https:\/\/t\.me\/([a-zA-Z0-9_]+|c\/\d+)\/\d+$"
    if not re.match(pattern, value):
        raise ValidationError(
            "Invalid Telegram message URL format. Example: https://t.me/channel_name/123456 or https://t.me/c/123456789/123456"
        )


class Cinema(AbstractBaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Name"), db_index=True)
    description = models.TextField(verbose_name=_("Description"), db_index=True)
    image = models.ImageField(
        upload_to="cinema", verbose_name=_("Image"), blank=True, null=True
    )
    country = models.ForeignKey(
        "Country",
        on_delete=models.PROTECT,
        verbose_name=_("Country"),
        db_index=True,
        related_name="cinemas_country",
    )
    language = models.ForeignKey(
        "Country",
        on_delete=models.PROTECT,
        verbose_name=_("Language"),
        db_index=True,
        related_name="cinemas_language",
    )
    genre = models.ManyToManyField("Genre", verbose_name=_("Genre"), db_index=True)
    resolution = models.ForeignKey(
        "Resolution",
        on_delete=models.PROTECT,
        verbose_name=_("Resolution"),
        db_index=True,
        related_name="cinemas_resolution",
    )
    year = models.ForeignKey(
        "Year", on_delete=models.PROTECT, verbose_name=_("Year"), db_index=True
    )
    code = models.PositiveBigIntegerField(verbose_name=_("Code"), db_index=True)
    channel = models.ForeignKey(
        "Channel", on_delete=models.PROTECT, verbose_name=_("Channel"), db_index=True
    )
    message_url = models.URLField(
        verbose_name=_("Message URL"),
        db_index=True,
        validators=[validate_telegram_message_url],
    )
    message_id = models.PositiveBigIntegerField(
        verbose_name=_("Message ID"), db_index=True, blank=True, null=True
    )
    file_id = models.CharField(
        max_length=255, verbose_name=_("File ID"), db_index=True, blank=True, null=True
    )
    view_count = models.PositiveIntegerField(
        verbose_name=_("View count"),
        default=0,
        db_index=True,
        editable=False,
        blank=True,
        null=True,
    )
    saved_count = models.PositiveIntegerField(
        verbose_name=_("Saved count"),
        default=0,
        db_index=True,
        editable=False,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_("Is active"), db_index=False
    )

    class Meta:
        verbose_name = _("Cinema")
        verbose_name_plural = _("Cinemas")
        db_table = "cinemas"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    def increment_views(self):
        """Ko'rishlar sonini oshirish uchun metod."""
        self.view_count += 1
        self.save(update_fields=["view_count"])
