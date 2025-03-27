from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import AutocompleteSelectFilter

from apps.backend.models.saved import Saved


@admin.register(Saved)
class SavedAdmin(ModelAdmin):
    list_display = ["id", "cinema", "user"]
    search_fields = ["cinema__title", "user__telegram_id"]
    list_filter = (
        ["cinema", AutocompleteSelectFilter],
        ["user", AutocompleteSelectFilter],
    )
    autocomplete_fields = ["cinema", "user"]
    list_per_page = 50
    list_filter_submit = True
