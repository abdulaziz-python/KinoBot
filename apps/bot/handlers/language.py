import time

from django.utils.translation import activate, gettext as _
from telebot import TeleBot, types
from telebot.types import CallbackQuery

from apps.backend.models.bot import BotUser, LanguageChoices
from apps.bot.keyboard import get_main_inline_buttons
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import set_language_code, with_language
from apps.bot.utils.subscription import check_subscribe


def callback_handler_language(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    logger.info(f"User {call.message.from_user.id} selected a language.")

    # Create buttons for Russian, Uzbek, and English languages
    uz_button = types.InlineKeyboardButton(text="O'zbek 🇺🇿", callback_data="lang_uz")
    ru_button = types.InlineKeyboardButton(text="Русский 🇷🇺", callback_data="lang_ru")
    en_button = types.InlineKeyboardButton(text="English 🇬🇧", callback_data="lang_en")
    back_button = types.InlineKeyboardButton(text=_("◀️Back"), callback_data="back")

    # Add buttons to the keyboard
    keyboard.add(uz_button, ru_button, en_button)
    keyboard.add(back_button)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Tilni tanlang / Выберите язык / Choose a language",
        reply_markup=keyboard,
    )


@with_language
def handle_language_selection(call: CallbackQuery, bot: TeleBot):
    user = BotUser.objects.get(telegram_id=call.from_user.id)
    logger.info(f"User {user.telegram_id} selected a language.")
    if check_subscribe(
        bot=bot,
        user_id=call.from_user.id,
        call=call,
    ):
        if call.data == "lang_ru":
            user.language_code = LanguageChoices.RU
        elif call.data == "lang_uz":
            user.language_code = LanguageChoices.UZ
        elif call.data == "lang_en":
            user.language_code = LanguageChoices.EN
        user.save()
        activate(set_language_code(call.from_user.id))
        msg = bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=_("Language updated successfully!"),
            parse_mode="Markdown",
            reply_markup=get_main_inline_buttons(),
        )
        time.sleep(3)
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
