from django.contrib.sites.models import Site
from django.utils.translation import gettext as _, activate
from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from apps.backend.models.info import Info
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import with_language, set_language_code
from apps.bot.utils.subscription import check_subscribe


@with_language
def callback_handler_info(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected a info.")
    if check_subscribe(
        bot=bot,
        user_id=call.from_user.id,
        call=call,
    ):
        buttons = [
            [InlineKeyboardButton(_("◀️Back"), callback_data="back")],
        ]
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(*[button for row in buttons for button in row])

        info = Info.objects.filter(is_active=True).first()
        if not info:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=_("No info available."),
                reply_markup=markup,
            )
            return

        current_domain = Site.objects.get_current().domain
        default_url = f"https://{current_domain}" + "/static/images/logo.png"
        thumbnail_url = (
            f"https://{current_domain}{info.image.url}" if info.image else default_url
        )
        caption = (
            f"<b>{info.title}</b>\n\n{info.description}<a href='{thumbnail_url}'>‎</a>"
        )

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=caption,
            parse_mode="HTML",
            reply_markup=markup,
        )
