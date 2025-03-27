from django.utils.translation import activate, gettext as _
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from apps.bot.utils.language import set_language_code
from apps.bot.utils.redis import set_user_session, get_user_session

PAGE_SIZE = 10


def send_paginated_cinema(
    chat_id: int,
    message_id: int,
    user_id: int,
    bot: TeleBot,
    page: int = 0,
    callback_query_id: str = None,
):
    """
    Show paginated files to the user and send inline buttons.
    """
    activate(set_language_code(user_id))
    session = get_user_session(user_id)
    if not session:
        bot.send_message(chat_id, _("You have no saved cinemas!"))
        return

    cinemas = session["cinemas"]
    total_cinemas = len(cinemas)
    total_pages = (total_cinemas - 1) // PAGE_SIZE + 1

    if page < 0 or page >= total_pages:
        if callback_query_id:
            bot.answer_callback_query(
                callback_query_id=callback_query_id,
                text=_("Page does not exist!"),
                show_alert=True,
            )
        return

    # Save the new page
    session["page"] = page
    set_user_session(user_id, cinemas, page)

    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    current_page_cinemas = cinemas[start_index:end_index]

    text = _("📂 Results {start}-{end} of {total}\n\n").format(
        start=start_index + 1, end=min(end_index, total_cinemas), total=total_cinemas
    )
    for i, f in enumerate(current_page_cinemas):
        text += _("<b>{index}.</b> {title} | 👁{view_count}\n").format(
            index=i + 1, title=f["title"], view_count=f["view_count"]
        )

    keyboard = InlineKeyboardMarkup(row_width=5)

    buttons = [
        InlineKeyboardButton(
            str(f"🎬{i + 1}"),
            callback_data=f"cinema_{f['id']}",
        )
        for i, f in enumerate(current_page_cinemas)
    ]
    keyboard.add(*buttons)

    nav_buttons = [
        InlineKeyboardButton("⬅", callback_data=f"page_nav:{page - 1}:{user_id}"),
        InlineKeyboardButton(_("🗑Clear"), callback_data="clear"),
        InlineKeyboardButton("➡", callback_data=f"page_nav:{page + 1}:{user_id}"),
    ]
    keyboard.row(*nav_buttons)
    keyboard.add(InlineKeyboardButton(_("◀️Back"), callback_data="back"))

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )
