from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.backend.models.bot import BotUser
from apps.shared.models.base import AbstractBaseModel


class DonationStatus(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    COMPLETED = "COMPLETED", _("Completed")
    FAILED = "FAILED", _("Failed")
    CANCELLED = "CANCELLED", _("Cancelled")


class Donation(AbstractBaseModel):
    user = models.ForeignKey(
        BotUser,
        on_delete=models.CASCADE,
        related_name="donations",
        verbose_name=_("User"),
    )
    amount = models.DecimalField(
        _("Amount"), max_digits=10, decimal_places=2, default=0
    )
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=DonationStatus,
        default=DonationStatus.PENDING,
    )
    transaction_id = models.CharField(
        _("Transaction ID"), max_length=255, null=True, blank=True
    )
    payment_url = models.URLField(_("Payment URL"), null=True, blank=True)
    completed_at = models.DateTimeField(_("Completed At"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Donation")
        verbose_name_plural = _("Donations")
        ordering = ("-created_at",)
        db_table = "donation"

    def __str__(self):
        return f"{self.user.telegram_id} - {self.amount} UZS" 