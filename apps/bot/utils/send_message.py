import os
import pathlib
from typing import Optional, Union

from django.conf import settings
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

    if image:
        try:
            if isinstance(image, str) and image.strip():
                image_path = None
                
                if image.startswith('/app/'):
                    image = image.replace('/app/', '')
                    
                if '/media/' in image:
                    relative_path = image.split('/media/')[-1]
                    image_path = os.path.join(settings.MEDIA_ROOT, relative_path)
                elif '/static/' in image:
                    relative_path = image.split('/static/')[-1]
                    image_path = os.path.join(settings.STATIC_ROOT, relative_path)
                elif image.startswith('/'):
                    image_path = image[1:]
                else:
                    image_path = image
                
                if image_path and os.path.exists(image_path):
                    bot.send_photo(
                        photo=open(image_path, 'rb'),
                        caption=text,
                        **common_args
                    )
                else:
                    bot.send_message(
                        text=f"{text}\n\n_(Image could not be loaded)_",
                        **common_args
                    )
            else:
                bot.send_photo(
                    photo=image,
                    caption=text,
                    **common_args
                )
        except Exception as e:
            bot.send_message(
                text=f"{text}\n\n_(Error loading image: {str(e)})_",
                **common_args
            )
    else:
        bot.send_message(
            text=text,
            **common_args
        )
