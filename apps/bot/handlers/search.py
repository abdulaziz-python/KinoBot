from django.utils.translation import gettext as _, activate
from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import with_language, set_language_code


@with_language
def callback_handler_search(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected a search.")

    buttons = [
        [InlineKeyboardButton(_("◀️Back"), callback_data="back")],
    ]
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(*[button for row in buttons for button in row])

    thumbnail_url = "https://child-protection.felixits.uz/media/avatars/PicsArt_25-03-26_10-50-34-589.png"

    text = _("🔍Send me cinema code")

    caption = f"<b>{text}</b>\n\n<a href='{thumbnail_url}'>‎</a>"
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=caption,
        parse_mode="HTML",
        reply_markup=markup,
    )
