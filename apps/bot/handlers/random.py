import random

from django.utils.translation import gettext_lazy as _, activate
from telebot import TeleBot
from telebot.types import CallbackQuery

from apps.backend.models.bot import BotUser
from apps.backend.models.cinema import Cinema
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import with_language, set_language_code
from apps.bot.utils.send_cinema import send_cinema
from apps.bot.utils.subscription import check_subscribe


@with_language
def callback_handler_random(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected a random.")
    if check_subscribe(
        bot=bot,
        user_id=call.from_user.id,
        call=call,
    ):
        user = BotUser.objects.filter(telegram_id=call.from_user.id).first()

        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            ids = list(
                Cinema.objects.filter(is_active=True).values_list("id", flat=True)
            )
            if not ids:
                bot.send_message(
                    call.message.chat.id, _("No available movies at the moment.")
                )
                return

            cinema = Cinema.objects.get(id=random.choice(ids))
            send_cinema(
                cinema_id=cinema.id,
                chat_id=call.message.chat.id,
                bot=bot,
                user=user,
            )

        except Exception as e:
            logger.exception(f"Error while processing random request {e}")
            bot.send_message(
                call.message.chat.id,
                text="Sorry, there was an error while processing your request.",
            )
