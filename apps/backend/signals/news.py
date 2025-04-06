from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.backend.models.news import News
from apps.backend.tasks.news import send_news_update_task


@receiver(post_save, sender=News)
def send_news_update(sender, instance, created, **kwargs):
    if created:
        try:
            send_news_update_task(instance.id)
        except Exception:
            pass
