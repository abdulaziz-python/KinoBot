from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from unfold.admin import ModelAdmin, TabularInline

from apps.backend.models.news import News, NewsButton


class NewsButtonInline(TabularInline, TranslationTabularInline):
    model = NewsButton
    extra = 1


@admin.register(News)
class NewsAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "title", "created_at", "updated_at"]
    list_per_page = 50
    search_fields = ["title"]
    list_filter = ["created_at", "updated_at"]
    inlines = [NewsButtonInline]


@admin.register(NewsButton)
class NewsButtonAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "title", "url", "created_at", "updated_at"]
    list_per_page = 50
    search_fields = ["title"]
    list_filter = ["created_at", "updated_at"]
    autocomplete_fields = ["news"]
