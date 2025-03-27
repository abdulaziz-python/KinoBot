from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.backend.models.country import Country


@admin.register(Country)
class CountryAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ["id", "name", "iso2", "emoji", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["name"]
    list_per_page = 50
    list_filter = ["is_active"]
    actions = ["make_active", "make_inactive"]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
