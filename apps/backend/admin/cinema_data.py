from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.backend.models.cinema_data import Genre, Year


@admin.register(Genre)
class GenreAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "name", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]
    list_per_page = 50


@admin.register(Year)
class YearAdmin(ModelAdmin):
    list_display = ["id", "year", "is_active"]
    search_fields = ["year"]
    list_filter = ["is_active"]
    list_per_page = 50
