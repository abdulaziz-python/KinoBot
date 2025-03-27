from telebot import TeleBot
from telebot.types import CallbackQuery

from apps.backend.models.cinema import Cinema
from apps.bot.utils.pagination import send_paginated_cinema
from apps.bot.utils.redis import get_user_session


def callback_cinema_select(call: CallbackQuery, bot: TeleBot):
    _, cinema_index_str, user_id_str = call.data.split(":")
    cinema_index = int(cinema_index_str)
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        bot.answer_callback_query(
            call.id, _("You don't have permissions"), show_alert=True
        )
        return

    session = get_user_session(user_id)
    if not session or cinema_index >= len(session["cinemas"]):
        bot.answer_callback_query(call.id, _("Cinema not found"), show_alert=True)
        return

    selected_cinema = session["cinemas"][cinema_index]
    caption = _("Selected cinema: {title}").format(file_name=selected_cinema["title"])
    cinema = Cinema.objects.get(id=selected_cinema["id"])
    bot.send_message(
        call.message.chat.id,
        text=caption,
    )


def callback_page_nav(call: CallbackQuery, bot: TeleBot):
    _, new_page_str, user_id_str = call.data.split(":")
    new_page = int(new_page_str)
    user_id = int(user_id_str)

    if call.from_user.id != user_id:
        bot.answer_callback_query(
            call.id, _("You cannot change this page!"), show_alert=True
        )
        return

    send_paginated_cinema(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        user_id=user_id,
        bot=bot,
        page=new_page,
    )

    bot.answer_callback_query(call.id)
