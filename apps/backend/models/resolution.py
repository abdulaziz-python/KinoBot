from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class Resolution(AbstractBaseModel):
    name = models.CharField(max_length=255, db_index=True, verbose_name=_("Name"))
    label = models.CharField(
        max_length=255, db_index=True, verbose_name=_("Label"), null=True, blank=True
    )
    width = models.PositiveIntegerField(verbose_name=_("Width"))
    height = models.PositiveIntegerField(verbose_name=_("Height"))
    bandwidth = models.PositiveIntegerField(verbose_name=_("Bandwidth"))

    class Meta:
        db_table = "resolutions"
        verbose_name = _("Resolution")
        verbose_name_plural = _("Resolutions")
        ordering = ["-width"]

    def __str__(self):
        return self.name
