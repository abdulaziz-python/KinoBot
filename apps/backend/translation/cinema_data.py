from modeltranslation.translator import TranslationOptions, register

from apps.backend.models.cinema_data import Genre


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ("name",)
