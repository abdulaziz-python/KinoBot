import time

from telebot import TeleBot
from telebot.types import Message
from django.utils.translation import activate, gettext as _

from apps.bot.utils.language import set_language_code

DATA = {}


def antispam_func(bot: TeleBot, message: Message):
    activate(set_language_code(message.from_user.id))
    bot.temp_data = {message.from_user.id: "OK"}
    if DATA.get(message.from_user.id):
        if int(time.time()) - DATA[message.from_user.id] < 2:
            bot.temp_data = {message.from_user.id: "FAIL"}
            bot.send_message(message.chat.id, _("You are making request too often"))
    DATA[message.from_user.id] = message.date
