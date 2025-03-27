from telebot.custom_filters import SimpleCustomFilter

from apps.backend.models.bot import BotUser, RoleChoices


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users
    """

    key = "admin"

    def check(self, message):
        admins = BotUser.objects.exclude(role=RoleChoices.USER).values_list(
            "telegram_id", flat=True
        )
        return message.from_user.id in admins
