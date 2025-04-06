from django.utils.translation import gettext as _
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from apps.backend.models.saved import Saved


def get_main_buttons():
    buttons = [
        [KeyboardButton(_("Language"))],
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[button for row in buttons for button in row])
    return markup


def get_main_inline_buttons():
    buttons = [
        [InlineKeyboardButton(_("🔍Search Cinema"), callback_data="search")],
        [InlineKeyboardButton(_("📊Top Cinema"), callback_data="top")],
        [InlineKeyboardButton(_("🎲Random"), callback_data="random")],
        [InlineKeyboardButton(_("📥Saved"), callback_data="saved")],
        [InlineKeyboardButton(_("⁉️Info"), callback_data="info")],
        [InlineKeyboardButton(_("🎭Genres"), callback_data="genres")],
        [InlineKeyboardButton(_("✅Language"), callback_data="language")],
        [InlineKeyboardButton(_("💸Donate"), callback_data="donate")],
    ]
    inline_button_search = InlineKeyboardButton(
        text=_("🎬✏️Search Cinema with text"), switch_inline_query_current_chat=""
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(*[button for row in buttons for button in row])
    markup.add(inline_button_search)
    return markup


def get_cinema_inline_buttons(cinema, user):
    is_saved = Saved.objects.filter(cinema=cinema, user=user).exists()
    buttons = [
        [InlineKeyboardButton(_("↪️Share"), switch_inline_query=f"{cinema.code}")],
        [
            InlineKeyboardButton(
                _("📥Save") if not is_saved else _("🗑️Unsave"),
                callback_data=f"save_{cinema.id}",
            )
        ],
        [InlineKeyboardButton(_("💸Donate"), callback_data="donate")],
        [InlineKeyboardButton(_("◀️Back"), callback_data="cinema_back")],
    ]
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(*[button for row in buttons for button in row])
    return markup
