from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.backend.models.cinema import Cinema
from apps.backend.tasks.cinema import process_cinema_task


@receiver(post_save, sender=Cinema)
def cinema_post_save(sender, instance, created, **kwargs):
    if created:
        process_cinema_task.delay(instance.id)
