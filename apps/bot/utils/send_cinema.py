from django.utils.translation import gettext as _
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import ReplyParameters

from apps.backend.models.channel import Channel, ChannelType
from apps.backend.models.cinema import Cinema
from apps.bot.keyboard import get_cinema_inline_buttons
from apps.bot.logger import logger
from apps.bot.utils.cinema_caption import cinema_caption


def get_draft_channel() -> Channel:
    draft_channel = Channel.objects.filter(channel_type=ChannelType.DRAFT).first()
    if not draft_channel:
        logger.error("No draft channel found.")
        raise ValueError("No draft channel found.")
    return draft_channel


def forward_message_to_draft(bot: TeleBot, cinema: Cinema, draft_chat_id: int):
    try:
        msg = bot.forward_message(
            from_chat_id=cinema.channel.channel_id,
            chat_id=draft_chat_id,
            message_id=cinema.message_id,
        )
    except ApiTelegramException as e:
        if e.result_json["description"] == "Bad Request: message to forward not found":
            logger.error(
                f"Message with ID {cinema.message_id} not found in chat {cinema.channel.channel_id}."
            )
            raise
        else:
            raise
    return msg


def send_cinema(cinema_id: int, chat_id: int, bot: TeleBot, user):
    try:
        cinema = Cinema.objects.get(id=cinema_id)
    except Cinema.DoesNotExist:
        logger.error(f"Cinema with ID {cinema_id} not found.")
        return

    if not cinema or not cinema.message_id or not cinema.channel or not cinema.file_id:
        bot.send_message(chat_id, _("The selected movie is unavailable."))
        return

    new_caption = cinema_caption(cinema_id=cinema.id, bot=bot)
    try:
        bot.send_video(
            chat_id,
            cinema.file_id,
            caption=new_caption,
            parse_mode="HTML",
            reply_markup=get_cinema_inline_buttons(cinema, user),
        )
    except ApiTelegramException as e:
        logger.exception(f"Error while sending video {e}")
        try:
            draft_channel = get_draft_channel()
            msg = forward_message_to_draft(bot, cinema, draft_channel.channel_id)
        except Exception as e:
            logger.error(f"Failed to forward message to draft channel: {e}")
            return

        bot.delete_message(chat_id=draft_channel.channel_id, message_id=msg.message_id)

        if not msg.video:
            bot.send_message(
                draft_channel.channel_id, _("Failed to retrieve the video.")
            )
            return

        cinema.file_id = msg.video.file_id
        cinema.is_active = True
        cinema.save()

        bot.send_video(
            chat_id,
            cinema.file_id,
            caption=new_caption,
            parse_mode="HTML",
            reply_markup=get_cinema_inline_buttons(cinema, user),
        )
    cinema.increment_views()
