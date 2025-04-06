from django.utils.translation import gettext as _, activate
from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from apps.backend.models.bot import BotUser
from apps.backend.models.donation import Donation
from apps.backend.tasks.payment import process_donation
from apps.bot.keyboard import get_main_inline_buttons
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.language import with_language, set_language_code
from apps.bot.utils.subscription import check_subscribe


@with_language
def callback_handler_donate(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected donate.")
    if check_subscribe(
        bot=bot,
        user_id=call.from_user.id,
        call=call,
    ):
        buttons = [
            [
                InlineKeyboardButton("5,000 UZS", callback_data="donate_amount_5000"),
                InlineKeyboardButton("10,000 UZS", callback_data="donate_amount_10000"),
            ],
            [
                InlineKeyboardButton("20,000 UZS", callback_data="donate_amount_20000"),
                InlineKeyboardButton("50,000 UZS", callback_data="donate_amount_50000"),
            ],
            [
                InlineKeyboardButton("100,000 UZS", callback_data="donate_amount_100000"),
                InlineKeyboardButton("O'zim kiritaman", callback_data="donate_amount_custom"),
            ],
            [InlineKeyboardButton(_("◀️Back"), callback_data="back")],
        ]
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(*[button for row in buttons for button in row])

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=_(
                "💸 *WTF Cinema loyihasini qo'llab-quvvatlang*\n\n"
                "Quyidagi summalardan birini tanlang yoki o'zingiz summa kiriting."
            ),
            parse_mode="Markdown",
            reply_markup=markup,
        )


@with_language
def callback_handler_donate_amount(call: CallbackQuery, bot: TeleBot):
    update_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        is_active=True,
    )
    activate(set_language_code(call.from_user.id))
    logger.info(f"User {call.from_user.id} selected donation amount.")
    
    amount_str = call.data.split("_")[-1]
    
    if amount_str == "custom":
        # O'z miqdorini kiritish uchun foydalanuvchiga so'rov yuborish
        msg = bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=_(
                "💸 *O'z xayriya miqdoringizni kiriting*\n\n"
                "Iltimos, xayriya miqdorini UZSda kiriting (minimal summa 1000 UZS).\n"
                "Masalan: 15000"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(_("◀️Back"), callback_data="donate")
            ),
        )
        
        # Foydalanuvchini summa kiritish rejimiga o'tkazish
        bot.register_next_step_handler(msg, process_custom_amount, bot)
    else:
        try:
            amount = int(amount_str)
            create_donation(call.from_user.id, amount, bot)
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=_(
                    "💸 *To'lov tayyorlanmoqda...*\n\n"
                    "Iltimos, kuting. To'lov tizimiga yo'naltirish tayyorlanmoqda."
                ),
                parse_mode="Markdown",
            )
        except ValueError:
            bot.answer_callback_query(call.id, _("Noto'g'ri summa kiritildi."))
            callback_handler_donate(call, bot)


def process_custom_amount(message, bot):
    try:
        amount = int(message.text.strip())
        
        if amount < 1000:
            bot.send_message(
                message.chat.id,
                _("Minimal summa 1000 UZS bo'lishi kerak. Iltimos, qayta urinib ko'ring."),
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(_("◀️Back"), callback_data="donate")
                ),
            )
            return
            
        create_donation(message.from_user.id, amount, bot)
        
        bot.send_message(
            message.chat.id,
            _(
                "💸 *To'lov tayyorlanmoqda...*\n\n"
                "Iltimos, kuting. To'lov tizimiga yo'naltirish tayyorlanmoqda."
            ),
            parse_mode="Markdown",
        )
    except ValueError:
        bot.send_message(
            message.chat.id,
            _("Iltimos, raqam kiriting. Masalan: 15000"),
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(_("◀️Back"), callback_data="donate")
            ),
        )


def create_donation(telegram_id, amount, bot):
    user = BotUser.objects.get(telegram_id=telegram_id)
    donation = Donation.objects.create(
        user=user,
        amount=amount
    )
    
    # Celery task orqali to'lovni ishga tushirish
    process_donation(donation.id) 