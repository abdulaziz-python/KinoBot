from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.backend.models.subscribe import SubscribeChannel, SubscribeChannelType
from apps.backend.tasks.subscribe import process_subscribe_channel_task


@receiver(post_save, sender=SubscribeChannel)
def check_channel_status(sender, instance, created, **kwargs):
    if created and instance.channel_type in [
        SubscribeChannelType.CHANNEL,
        SubscribeChannelType.GROUP,
    ]:
        try:
            process_subscribe_channel_task(instance.id)
        except Exception:
            pass
