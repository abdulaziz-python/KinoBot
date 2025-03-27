from django.utils.translation import gettext as _, activate
from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from apps.backend.models.bot import BotUser
from apps.backend.models.cinema import Cinema
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import with_language, set_language_code
from apps.bot.utils.send_cinema import send_cinema


@with_language
def callback_handler_top(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected a top.")
    cinemas = Cinema.objects.filter(is_active=True).order_by("-view_count")[:10]
    markup = InlineKeyboardMarkup(row_width=5)
    indexes = []
    text = _("Top 10 cinemas:\n\n")
    for index, cinema in enumerate(cinemas):
        text += f"\n<b>{index + 1}.</b> {cinema.title} | 👁{cinema.view_count}"
        indexes.append(index + 1)
    buttons = [
        [
            InlineKeyboardButton(
                f"🎬 {index}", callback_data=f"cinema_{cinemas[index - 1].id}"
            )
            for index in indexes
        ]
    ]
    markup.add(*[button for row in buttons for button in row])
    markup.add(InlineKeyboardButton(_("◀️Back"), callback_data="back"))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode="HTML",
        reply_markup=markup,
    )


@with_language
def callback_handler_top_cinema(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    logger.info(f"User {call.from_user.id} selected a top.")

    cinema_id = call.data.split("_")[1]
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        try:
            cinema = Cinema.objects.get(id=cinema_id)
        except Cinema.DoesNotExist:
            bot.send_message(
                call.message.chat.id,
                _("Sorry, the cinema you are looking for does not exist."),
            )
            return
        user = BotUser.objects.filter(telegram_id=call.from_user.id).first()
        send_cinema(
            cinema_id=cinema.id,
            chat_id=call.message.chat.id,
            bot=bot,
            user=user,
        )

    except Exception as e:
        logger.exception(f"Error while processing random request {e}")
        bot.send_message(
            call.message.chat.id,
            _("Sorry, there was an error while processing your request."),
        )
