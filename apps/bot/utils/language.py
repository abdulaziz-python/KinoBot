from functools import wraps

from django.utils.translation import activate
from telebot.types import Message, CallbackQuery

from apps.backend.models.bot import BotUser


def set_language_code(telegram_id):
    if BotUser.objects.filter(telegram_id=telegram_id).exists():
        user = BotUser.objects.get(telegram_id=telegram_id)
        activate(user.language_code)
        return user.language_code
    else:
        return "uz"


def with_language(func):
    """
    Decorator that sets the language for the incoming message or callback.
    It expects that either a Message or a CallbackQuery (with a message attribute)
    is passed as the first positional argument.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        message = None
        # Check if a Message is passed directly
        for arg in args:
            if isinstance(arg, Message):
                message = arg
                break
            if isinstance(arg, CallbackQuery):
                message = arg.message
                break
        if message:
            activate(set_language_code(message.from_user.id))
        return func(*args, **kwargs)

    return wrapper
