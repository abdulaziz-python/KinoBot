import time
import uuid

from django.utils.translation import gettext as _, activate
from telebot import TeleBot
from telebot.types import CallbackQuery

from apps.backend.models.bot import BotUser
from apps.backend.models.saved import Saved
from apps.bot.keyboard import get_main_inline_buttons
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import with_language, set_language_code
from apps.bot.utils.pagination import send_paginated_cinema
from apps.bot.utils.redis import set_user_session


def callback_handler_saved(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected a saved.")

    user = BotUser.objects.filter(telegram_id=call.from_user.id).first()
    saved_cinemas = list(Saved.objects.filter(user=user))

    if not saved_cinemas:
        bot.answer_callback_query(call.id, _("❌ No saved cinema."), show_alert=True)
        return

    set_user_session(call.from_user.id, saved_cinemas, page=0)

    current_message = call.message.text
    new_message = _("Loading...")

    if current_message == new_message:
        new_message = f"{uuid.uuid4()}"
    sent_message = bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=new_message,
        parse_mode="HTML",
        reply_markup=get_main_inline_buttons(),
    )
    send_paginated_cinema(
        chat_id=call.message.chat.id,
        message_id=sent_message.message_id,
        user_id=call.from_user.id,
        bot=bot,
        page=0,
    )


@with_language
def callback_handler_clear(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected a info.")

    user = BotUser.objects.filter(telegram_id=call.from_user.id).first()
    saved_cinemas = Saved.objects.filter(user=user)
    if not saved_cinemas:
        bot.answer_callback_query(call.id, _("❌No saved cinema."), show_alert=True)
        return

    saved_cinemas.delete()

    text = _("❌Saved cinemas cleared.")
    bot.answer_callback_query(call.id, text=text, show_alert=True)
    msg = bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode="HTML",
        reply_markup=get_main_inline_buttons(),
    )
    time.sleep(5)
    first_name = call.from_user.first_name
    if call.from_user.last_name:
        first_name += f" {call.from_user.last_name}"
    caption = _("[{}](tg://user?id={}) Welcome to the bot!").format(
        first_name, call.from_user.id
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=msg.message_id,
        text=caption,
        parse_mode="Markdown",
        reply_markup=get_main_inline_buttons(),
    )
