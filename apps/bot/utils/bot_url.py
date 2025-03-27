import telebot


def get_bot_url(bot: telebot.TeleBot) -> str:
    bot_info = bot.get_me()
    bot_username = bot_info.username
    bot_url = f"https://t.me/{bot_username}"
    return bot_url


def get_bot_username(bot: telebot.TeleBot) -> str:
    bot_info = bot.get_me()
    bot_username = bot_info.username
    return bot_username
