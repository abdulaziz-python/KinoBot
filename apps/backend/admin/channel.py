from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from apps.backend.models.channel import Channel


@admin.register(Channel)
class ChannelAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ["id", "name", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["name"]
    list_per_page = 50
    list_filter = ["is_active"]
