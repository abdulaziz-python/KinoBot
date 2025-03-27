from django.utils.translation import gettext as _, activate
from telebot import TeleBot
from telebot.types import CallbackQuery

from apps.bot.keyboard import get_main_inline_buttons
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import with_language, set_language_code
from apps.bot.utils.redis import delete_user_session
from apps.bot.utils.subscription import check_subscribe


def callback_handler_confirm_subscription(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected a back.")
    if check_subscribe(
        bot=bot,
        user_id=call.from_user.id,
        call=call,
    ):
        first_name = call.from_user.first_name
        if call.from_user.last_name:
            first_name += f" {call.from_user.last_name}"

        caption = _("[{}](tg://user?id={}) Welcome to the bot!").format(
            first_name, call.from_user.id
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=caption,
            parse_mode="Markdown",
            reply_markup=get_main_inline_buttons(),
        )
