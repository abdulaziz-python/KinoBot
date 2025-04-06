from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from apps.backend.models.donation import Donation


@admin.register(Donation)
class DonationAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ["id", "user", "amount", "status", "created_at", "completed_at"]
    list_filter = ["status"]
    search_fields = ["user__telegram_id", "transaction_id"]
    readonly_fields = ["transaction_id", "payment_url", "completed_at"]
    list_per_page = 50 