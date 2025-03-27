from django.utils.translation import gettext as _, activate
from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from apps.backend.models.bot import BotUser
from apps.backend.models.cinema import Cinema
from apps.backend.models.info import Info
from apps.backend.models.saved import Saved
from apps.bot.keyboard import get_cinema_inline_buttons
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import with_language, set_language_code


@with_language
def callback_handler_save(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected a save.")

    cinema_id = call.data.split("_")[1]
    cinema = Cinema.objects.get(id=cinema_id)
    user = BotUser.objects.filter(telegram_id=call.from_user.id).first()
    is_saved = Saved.objects.filter(cinema=cinema, user=user).exists()
    if is_saved:
        Saved.objects.filter(cinema=cinema, user=user).delete()
        bot.answer_callback_query(call.id, _("Cinema has been unsaved."))
    else:
        Saved.objects.create(cinema=cinema, user=user)
        bot.answer_callback_query(call.id, _("Cinema has been saved."))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=get_cinema_inline_buttons(cinema, user),
    )
