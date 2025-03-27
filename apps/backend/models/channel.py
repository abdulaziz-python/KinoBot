from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class ChannelType(models.TextChoices):
    TARGET = "TARGET", _("Target")
    SOURCE = "SOURCE", _("Source")
    DRAFT = "DRAFT", _("Draft")


class Channel(AbstractBaseModel):
    name = models.CharField(_("Name"), max_length=255, null=True, blank=True)
    url = models.CharField(_("URL"), max_length=255, null=True, blank=True)
    channel_id = models.CharField(
        _("Channel ID"), max_length=255, null=True, blank=True
    )
    username = models.CharField(_("Username"), max_length=255, null=True, blank=True)
    channel_type = models.CharField(
        _("Channel Type"),
        max_length=50,
        choices=ChannelType,
        default=ChannelType.SOURCE,
    )
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")
        ordering = ("-created_at",)
        db_table = "channel"

    def __str__(self):
        return self.name
