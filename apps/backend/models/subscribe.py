from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class SubscribeChannelType(models.TextChoices):
    CHANNEL = "CHANNEL", _("Channel")
    GROUP = "GROUP", _("Group")
    BOT = "BOT", _("Bot")


class SubscribeChannel(AbstractBaseModel):
    name = models.CharField(_("Name"), max_length=255, null=True, blank=True)
    url = models.CharField(_("URL"), max_length=255, null=True, blank=True)
    channel_id = models.CharField(
        _("Channel ID"), max_length=255, null=True, blank=True
    )
    channel_type = models.CharField(
        _("Channel Type"),
        max_length=50,
        choices=SubscribeChannelType,
        default=SubscribeChannelType.CHANNEL,
    )
    username = models.CharField(_("Username"), max_length=255, null=True, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Subscribe Channel")
        verbose_name_plural = _("Subscribe Channel")
        ordering = ("-created_at",)
        db_table = "subscribe_channel"

    def __str__(self):
        return f"ID: {self.id}"
