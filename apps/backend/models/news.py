from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models.base import AbstractBaseModel


class News(AbstractBaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    image = models.ImageField(
        upload_to="news", verbose_name=_("Image"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ("-created_at",)
        db_table = "news"

    def __str__(self):
        return str(self.title)


class NewsButton(AbstractBaseModel):
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, verbose_name=_("News"), related_name="buttons"
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    url = models.URLField(verbose_name=_("URL"))

    class Meta:
        verbose_name = _("News Button")
        verbose_name_plural = _("News Buttons")
        db_table = "news_buttons"

    def __str__(self):
        return str(self.title)
