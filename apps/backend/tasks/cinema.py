import logging
import os
import re
import time

import telebot
from celery import shared_task
from django.utils.translation import gettext as _
from telebot import TeleBot

from apps.backend.models.channel import Channel, ChannelType
from apps.backend.models.cinema import Cinema

# Logger
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(TOKEN)


def extract_last_number(url: str) -> int | None:
    """Extracts the last number from a URL."""
    match = re.search(r"/(\d+)$", url)
    return int(match.group(1)) if match else None


@shared_task
def process_cinema_task(cinema_id: int) -> None:
    """Processes a cinema object by forwarding its message and updating its file ID."""
    time.sleep(1)
    try:
        cinema = Cinema.objects.select_related("channel").get(id=cinema_id)
        chat_id = cinema.channel.channel_id
        draft_channel = Channel.objects.filter(channel_type=ChannelType.DRAFT).first()
        cinema.message_id = extract_last_number(cinema.message_url) or cinema.message_id
        cinema.code = cinema.id
        cinema.save(update_fields=["message_id", "code"])

        if not draft_channel:
            logger.error("No draft channel found.")
            return

        draft_chat_id = draft_channel.channel_id

        try:
            msg = bot.forward_message(
                from_chat_id=chat_id,
                chat_id=draft_chat_id,
                message_id=cinema.message_id,
            )
        except telebot.apihelper.ApiTelegramException as e:
            if (
                e.result_json["description"]
                == "Bad Request: message to forward not found"
            ):
                logger.error(
                    f"Message with ID {cinema.message_id} not found in chat {chat_id}."
                )
                return
            else:
                raise

        bot.delete_message(chat_id=draft_chat_id, message_id=msg.message_id)

        if not msg.video:
            bot.send_message(draft_chat_id, _("Failed to retrieve the video."))
            return

        cinema.file_id = msg.video.file_id
        cinema.is_active = True
        cinema.save()

        logger.info(f"Cinema {cinema_id} processed successfully.")
    except Cinema.DoesNotExist:
        logger.error(f"Cinema with ID {cinema_id} does not exist.")
    except Exception as e:
        logger.exception(f"Error processing cinema {cinema_id}: {e}")
