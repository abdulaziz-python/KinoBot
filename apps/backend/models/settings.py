from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class SettingsManager(models.Manager):
    def get_from_key(self, key, default=False):
        obj = self.filter(key=key)
        if obj.exists():
            return obj.first().value
        return default


class Settings(AbstractBaseModel):
    key = models.CharField(max_length=100, verbose_name=_("Key"))
    value = models.BooleanField(
        default=False, verbose_name=_("ON/OFF"), null=True, blank=True
    )
    label = models.CharField(
        max_length=255, verbose_name=_("Label"), null=True, blank=True
    )

    objects = SettingsManager()

    class Meta:
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")
        ordering = ("-created_at",)
