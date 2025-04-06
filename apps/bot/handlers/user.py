import re

from django.utils.translation import gettext as _, activate
from telebot import TeleBot
from telebot.types import (
    Message,
    ReactionTypeEmoji,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from apps.backend.models.bot import BotUser
from apps.backend.models.cinema import Cinema
from apps.backend.models.subscribe import SubscribeChannel
from apps.backend.tasks.payment import update_donation_status
from apps.bot.keyboard import get_main_inline_buttons
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import with_language, set_language_code
from apps.bot.utils.send_cinema import send_cinema
from apps.bot.utils.subscription import check_subscribe


@with_language
def any_user(message: Message, bot: TeleBot):
    try:
        update_or_create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            is_active=True,
        )
        activate(set_language_code(message.from_user.id))
        logger.info(f"User {message.from_user.id} started the bot.")

        bot.set_message_reaction(
            message.chat.id, message.message_id, [ReactionTypeEmoji("❤️")], is_big=True
        )

        if check_subscribe(
            bot=bot,
            user_id=message.from_user.id,
            message=message,
        ):
            # Tekshirish: /start buyruq payment callback bilan kelganmi?
            if message.text.startswith("/start payment_"):
                if message.text.startswith("/start payment_success_"):
                    transaction_id = message.text.replace("/start payment_success_", "")
                    update_donation_status.delay(transaction_id, "success")
                    bot.send_message(
                        message.chat.id,
                        _("*To'lovingiz qabul qilinmoqda...*\n\nBir necha soniya ichida to'lov natijasi haqida xabar olasiz."),
                        parse_mode="Markdown",
                        reply_markup=get_main_inline_buttons(),
                    )
                    return
                elif message.text.startswith("/start payment_cancel_"):
                    transaction_id = message.text.replace("/start payment_cancel_", "")
                    update_donation_status.delay(transaction_id, "cancelled")
                    bot.send_message(
                        message.chat.id,
                        _("*To'lov bekor qilindi*\n\nBoshqa vaqt urinib ko'rishingiz mumkin."),
                        parse_mode="Markdown",
                        reply_markup=get_main_inline_buttons(),
                    )
                    return

            # Oddiy /start buyrug'i yoki ID bilan kelgan /start
            if message.text.startswith("/start ") and re.match(
                r"/start \d+", message.text
            ):
                cinema_id = message.text.split(" ")[1]
                user = BotUser.objects.filter(telegram_id=message.from_user.id).first()
                try:
                    cinema = Cinema.objects.get(id=cinema_id)
                except Cinema.DoesNotExist:
                    bot.send_message(message.chat.id, _("Cinema not found."))
                    return
                send_cinema(
                    cinema_id=cinema.id,
                    chat_id=message.chat.id,
                    bot=bot,
                    user=user,
                )
            else:
                first_name = message.from_user.first_name
                if message.from_user.last_name:
                    first_name += f" {message.from_user.last_name}"

                bot.send_message(
                    message.chat.id,
                    _("[{}](tg://user?id={}) Welcome to the bot!").format(
                        first_name, message.from_user.id
                    ),
                    parse_mode="Markdown",
                    reply_markup=get_main_inline_buttons(),
                )
    except Exception as e:
        bot.send_message(message.chat.id, _("An error occurred."))
        logger.error(f"Error in any_user: {e}")
