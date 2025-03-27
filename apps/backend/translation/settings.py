from modeltranslation.translator import TranslationOptions, register

from apps.backend.models.settings import Settings


@register(Settings)
class SettingsTranslationOptions(TranslationOptions):
    fields = ("label",)
