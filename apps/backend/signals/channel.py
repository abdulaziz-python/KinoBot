from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.backend.models.channel import Channel
from apps.backend.tasks.channel import process_channel_task


@receiver(post_save, sender=Channel)
def channel_post_save(sender, instance, created, **kwargs):
    if created:
        process_channel_task.delay(instance.id)
