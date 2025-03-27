from modeltranslation.translator import TranslationOptions, register

from apps.backend.models.cinema import Cinema


@register(Cinema)
class CinemaTranslationOptions(TranslationOptions):
    fields = ("title", "description")
