from django.utils.translation import gettext as _
from telebot.apihelper import ApiTelegramException
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from apps.backend.models.settings import Settings
from apps.backend.models.subscribe import SubscribeChannel, SubscribeChannelType


def check_subscribe(bot, user_id, call=None, message=None):
    """
    Foydalanuvchining homiy kanallarga obuna bo'lganligini tekshiradi.
    Agar obuna bo'lmagan bo'lsa, unga ogohlantirish xabarini yuboradi.

    :param bot: Telebot obyekti
    :param user_id: Foydalanuvchi IDsi
    :param call: (Optional) CallbackQuery obyekti
    :param message: (Optional) Message obyekti
    :return: Agar foydalanuvchi hamma kanallarga obuna bo'lgan bo‘lsa, True; aks holda False
    """
    switcher = Settings.objects.get_from_key("bot:subscribe")
    if switcher:
        channels = SubscribeChannel.objects.filter(
            is_active=True,
            channel_type__in=[SubscribeChannelType.CHANNEL, SubscribeChannelType.GROUP],
        )

        for channel in channels:
            try:
                username = f"@{channel.username}"
                chat_member = bot.get_chat_member(username, user_id)

                if chat_member.status not in ["member", "administrator", "creator"]:
                    alert_text = _(
                        f"❗️Siz homiy kanallarga hali obuna bo'lmadingiz, kanallarga obuna bo'ling va Tasdiqlash tugmasini bosing.\n\n"
                        f"{channel.name} ga obuna bo'ling"
                    )
                    subscribe_channels = SubscribeChannel.objects.filter(is_active=True)
                    buttons = [
                        InlineKeyboardButton(
                            text=subscribe_channel.name, url=subscribe_channel.url
                        )
                        for subscribe_channel in subscribe_channels
                    ]
                    confirm = InlineKeyboardButton(
                        text=_("✅Confirm"), callback_data="confirm_subscription"
                    )
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    keyboard.add(*buttons)
                    keyboard.add(confirm)

                    if call:
                        bot.answer_callback_query(call.id, alert_text, show_alert=True)
                        bot.delete_message(
                            call.message.chat.id, call.message.message_id
                        )
                        bot.send_message(
                            call.message.chat.id, alert_text, reply_markup=keyboard
                        )
                    elif message:
                        bot.send_message(
                            message.chat.id, alert_text, reply_markup=keyboard
                        )

                    return False  # Agar foydalanuvchi birorta kanalga obuna bo'lmagan bo‘lsa, False qaytaramiz

            except ApiTelegramException as e:
                error_text = _("Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
                if e.error_code == 400:
                    if "query is too old" in e.result_json.get("description", ""):
                        error_text = _(
                            "Xatolik yuz berdi: so'rov eskirgan. Iltimos, qayta urinib ko'ring."
                        )
                    else:
                        error_text = _(
                            f"Xatolik yuz berdi: chat topilmadi. Bot {username} kanalida admin qilinmagan. Iltimos, keyinroq urinib ko'ring."
                        )

                if call:
                    bot.answer_callback_query(call.id, error_text, show_alert=True)
                elif message:
                    bot.send_message(message.chat.id, error_text)

                return False  # Agar xatolik bo'lsa, False qaytaramiz

        return (
            True  # Agar foydalanuvchi barcha kanallarga obuna bo'lsa, True qaytaramiz
        )
    return True  # Agar bot sozlamalari ichida obuna tekshirish o'chirilgan bo'lsa, True qaytaramiz
