from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class Genre(AbstractBaseModel):
    name = models.CharField(
        max_length=255, unique=True, db_index=True, verbose_name=_("Name")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        db_table = "genre"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Year(AbstractBaseModel):
    year = models.IntegerField(unique=True, verbose_name=_("Year"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    class Meta:
        verbose_name = _("Year")
        verbose_name_plural = _("Years")
        db_table = "years"
        ordering = ["-year"]

    def __str__(self):
        return str(self.year)
