from django.utils.translation import gettext as _, activate
from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from apps.backend.models.cinema import Cinema
from apps.backend.models.cinema_data import Genre
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import with_language, set_language_code


@with_language
def callback_handler_genre(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected a genre.")

    genres = Genre.objects.filter(is_active=True)
    buttons = [
        [
            InlineKeyboardButton(genre.name, callback_data=f"genre_{genre.id}")
            for genre in genres
        ],
    ]
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(*[button for row in buttons for button in row])
    markup.add(InlineKeyboardButton(_("◀️Back"), callback_data="back"))

    if not genres:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=_("No genre available."),
            reply_markup=markup,
        )
        return

    caption = _("All genres:")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=caption,
        parse_mode="Markdown",
        reply_markup=markup,
    )


@with_language
def callback_handler_genre_cinema(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected a genre.")

    genre_id = call.data.split("_")[1]

    genre = Genre.objects.get(id=genre_id)
    cinemas_count = Cinema.objects.filter(genre__id=genre_id).count()
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton(
            _("List of Cinemas📋"), switch_inline_query_current_chat=f"#{genre.name}"
        )
    )
    markup.add(InlineKeyboardButton(_("◀️Back"), callback_data="back"))

    caption = _("Find {cinemas_count} cinemas with this genre.").format(
        cinemas_count=cinemas_count
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=caption,
        parse_mode="Markdown",
        reply_markup=markup,
    )
