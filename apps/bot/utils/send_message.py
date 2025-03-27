import pathlib
from typing import Optional, Union

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InputFile


def send_reply(
    bot: TeleBot,
    user_id: int,
    text: str,
    reply_markup: Optional[InlineKeyboardMarkup] = None,
    image: Optional[Union[str, InputFile]] = None,
) -> None:
    common_args = {
        "chat_id": user_id,
        "parse_mode": "Markdown",
    }
    if reply_markup:
        common_args["reply_markup"] = reply_markup

    valid_image = None
    if image:
        if isinstance(image, str) and image.strip():
            valid_image = image
        elif not isinstance(image, str):
            valid_image = image

    if image:
        bot.send_photo(
            photo=InputFile(pathlib.Path(f"/app/assets{valid_image}")),
            caption=text,
            **common_args,
        )
    else:
        bot.send_message(text=text, **common_args)
