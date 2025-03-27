from telebot import TeleBot
from telebot.types import CallbackQuery

from apps.bot.utils.pagination import send_paginated_cinema
from apps.bot.utils.subscription import check_subscribe


def callback_page_nav(call: CallbackQuery, bot: TeleBot):
    _, new_page_str, user_id_str = call.data.split(":")
    new_page = int(new_page_str)
    user_id = int(user_id_str)
    if check_subscribe(
        bot=bot,
        user_id=call.from_user.id,
        call=call,
    ):

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
