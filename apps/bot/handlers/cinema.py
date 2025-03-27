import re

from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot.types import Message

from apps.backend.models.bot import BotUser
from apps.backend.models.cinema import Cinema
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import set_language_code
from apps.bot.utils.send_cinema import send_cinema
from apps.bot.utils.subscription import check_subscribe


def handle_message(message: Message, bot: TeleBot):
    """Handle incoming messages"""
    activate(set_language_code(message.from_user.id))
    update_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        is_active=True,
    )
    logger.info(f"User {message.from_user.id} send cinema code.")
    if check_subscribe(
        bot=bot,
        user_id=message.from_user.id,
        message=message,
    ):
        user = BotUser.objects.filter(telegram_id=message.from_user.id).first()

        if re.match(r"\d+", message.text):
            cinema_id = message.text
            logger.debug(f"Cinema code: {cinema_id}")
            try:
                cinema = Cinema.objects.get(code=cinema_id)
            except Cinema.DoesNotExist:
                bot.send_message(message.chat.id, _("Cinema not found."))
                return
            send_cinema(
                cinema_id=cinema.id,
                chat_id=message.chat.id,
                bot=bot,
                user=user,
            )
        elif message.via_bot and message.via_bot.id == bot.get_me().id:
            try:
                message_data = message.json
                reply_markup = message_data.get("reply_markup", {})

                if "inline_keyboard" in reply_markup:
                    for row in reply_markup["inline_keyboard"]:
                        for button in row:
                            if "switch_inline_query" in button:
                                query_data = button["switch_inline_query"]
                                send_cinema(
                                    cinema_id=int(query_data),
                                    chat_id=message.chat.id,
                                    bot=bot,
                                    user=user,
                                )

            except Exception as e:
                logger.error(f"Error: {e}")
            try:
                bot.delete_message(message.chat.id, message.message_id)
                logger.info(
                    f"Deleted message {message.message_id} from chat {message.chat.id}"
                )
            except Exception as e:
                logger.error(
                    f"Failed to delete message {message.message_id} from chat {message.chat.id}: {e}"
                )
