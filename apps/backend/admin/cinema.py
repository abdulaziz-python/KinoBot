from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import AutocompleteSelectFilter

from apps.backend.models.cinema import Cinema


@admin.register(Cinema)
class CinemaAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = [
        "id",
        "title",
        "message_id",
        "code",
        "view_count",
        "saved_count",
        "is_active",
    ]
    search_fields = ["title", "description"]
    autocomplete_fields = [
        "country",
        "language",
        "genre",
        "resolution",
        "year",
        "channel",
    ]
    list_per_page = 50
    list_filter = (
        ["country", AutocompleteSelectFilter],
        ["language", AutocompleteSelectFilter],
        ["genre", AutocompleteSelectFilter],
        ["resolution", AutocompleteSelectFilter],
        ["year", AutocompleteSelectFilter],
        ["channel", AutocompleteSelectFilter],
    )
    readonly_fields = [
        "code",
        "view_count",
        "saved_count",
        "created_at",
        "updated_at",
        "message_id",
        "file_id",
    ]
    list_filter_submit = True
