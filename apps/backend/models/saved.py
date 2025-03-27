from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class Saved(AbstractBaseModel):
    cinema = models.ForeignKey(
        "Cinema",
        on_delete=models.CASCADE,
        related_name="saves",
        verbose_name=_("cinema"),
    )
    user = models.ForeignKey(
        "BotUser", on_delete=models.CASCADE, verbose_name=_("User")
    )

    class Meta:
        verbose_name = _("Saved cinema")
        verbose_name_plural = _("Saved cinemas")
        unique_together = ["cinema", "user"]
        ordering = ["-created_at"]
        db_table = "saves"

    def __str__(self):
        return f"{self.user} {self.cinema}"
