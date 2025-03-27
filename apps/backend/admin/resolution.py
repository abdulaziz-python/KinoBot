from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.backend.models.resolution import Resolution


@admin.register(Resolution)
class ResolutionAdmin(ModelAdmin):
    list_display = ["id", "name", "width", "height", "bandwidth", "label"]
    search_fields = ["name"]
    list_per_page = 50
