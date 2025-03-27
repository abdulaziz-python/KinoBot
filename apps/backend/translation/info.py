from modeltranslation.translator import TranslationOptions, register

from apps.backend.models.info import Info


@register(Info)
class InfoTranslationOptions(TranslationOptions):
    fields = ("title", "description")
