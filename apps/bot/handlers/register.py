from django.utils.translation import gettext as _
from telebot import TeleBot
from telebot.types import CallbackQuery

from apps.bot.handlers.back import callback_handler_back, callback_handler_cinema_back
from apps.bot.handlers.confirm_subscription import callback_handler_confirm_subscription
from apps.bot.handlers.genres import (
    callback_handler_genre,
    callback_handler_genre_cinema,
)
from apps.bot.handlers.info import callback_handler_info
from apps.bot.handlers.language import (
    handle_language_selection,
    callback_handler_language,
)
from apps.bot.handlers.pagination import callback_page_nav
from apps.bot.handlers.random import callback_handler_random
from apps.bot.handlers.save import callback_handler_save
from apps.bot.handlers.saved import callback_handler_saved, callback_handler_clear
from apps.bot.handlers.search import callback_handler_search
from apps.bot.handlers.top import callback_handler_top, callback_handler_top_cinema
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import with_language


@with_language
def handle_callback_query(call: CallbackQuery, bot: TeleBot):
    logger.info(
        f"User {call.data} -**- {call.from_user.id} ===================================="
    )
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    if call.data == "lang_ru" or call.data == "lang_uz" or call.data == "lang_en":
        handle_language_selection(call, bot)
    elif call.data == "info":
        callback_handler_info(call, bot)
    elif call.data == "search":
        callback_handler_search(call, bot)
    elif call.data == "top":
        callback_handler_top(call, bot)
    elif call.data == "random":
        callback_handler_random(call, bot)
    elif call.data == "saved":
        callback_handler_saved(call, bot)
    elif call.data == "genres":
        callback_handler_genre(call, bot)
    elif call.data == "language":
        callback_handler_language(call, bot)
    elif call.data == "back":
        callback_handler_back(call, bot)
    elif call.data == "cinema_back":
        callback_handler_cinema_back(call, bot)
    elif call.data == "clear":
        callback_handler_clear(call, bot)
    elif call.data.startswith("save_"):
        callback_handler_save(call, bot)
    elif call.data.startswith("genre_"):
        callback_handler_genre_cinema(call, bot)
    elif call.data.startswith("cinema_"):
        callback_handler_top_cinema(call, bot)
    elif call.data.startswith("page_nav"):
        callback_page_nav(call, bot)
        logger.info(f"User {call.data} selected a page.")
    elif call.data == "confirm_subscription":
        callback_handler_confirm_subscription(call, bot)
    else:
        bot.answer_callback_query(call.id, _("Unknown action."))
        logger.info(f"User {call.from_user.id} performed an unknown action.")
