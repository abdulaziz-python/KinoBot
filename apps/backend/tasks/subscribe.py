import logging
import os

from celery import shared_task
from telebot import TeleBot

from apps.backend.models.subscribe import SubscribeChannel

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

logger = logging.getLogger(__name__)


def fetch_channel_data(channel_username: str) -> dict | None:
    try:
        channel_username = f"@{channel_username}"
        chat = bot.get_chat(channel_username)
        return {"id": chat.id, "username": chat.username, "name": chat.title}
    except Exception as e:
        logger.error(f"Kanal ma'lumotlarini olishda xatolik: {channel_username} -> {e}")
        return None


@shared_task
def process_subscribe_channel_task(subscribe_channel_id: int) -> None:
    try:
        instance = SubscribeChannel.objects.get(id=subscribe_channel_id)
        url = instance.url.split("/")[-1]

        channel_data = fetch_channel_data(url)
        if channel_data:
            instance.channel_id = channel_data["id"]
            instance.username = channel_data["username"]
            instance.name = channel_data["name"]
            instance.save(update_fields=["channel_id", "username", "name"])

            logger.info(
                f"Kanal yangilandi: ID={instance.channel_id}, Name={instance.name}"
            )
        else:
            logger.warning(f"Kanal ma'lumotlarini olishning imkoni bo‘lmadi: {url}")

    except SubscribeChannel.DoesNotExist:
        logger.error(f"SubscribeChannel obyekt topilmadi: ID={subscribe_channel_id}")
    except Exception as e:
        logger.exception(f"process_subscribe_channel_task bajarishda xatolik: {e}")
