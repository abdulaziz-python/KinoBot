import logging
import os
import time
import uuid
from datetime import datetime

import requests
from celery import shared_task
from django.conf import settings
from django.utils.translation import activate
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.backend.models.bot import BotUser
from apps.backend.models.donation import Donation, DonationStatus
from apps.bot.utils.language import set_language_code

bot = TeleBot(os.getenv("BOT_TOKEN"))
logger = logging.getLogger(__name__)

STARS_PAYMENT_URL = "https://api.stars.uz/v1/payment/merchant/create-invoice"
STARS_API_KEY = os.getenv("STARS_API_KEY", "YOUR_STARS_API_KEY")


def create_payment_link(amount, user_id, success_url=None, cancel_url=None):
    try:
        transaction_id = str(uuid.uuid4())
        
        headers = {
            "Authorization": f"Bearer {STARS_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "amount": float(amount),
            "external_id": transaction_id,
            "description": f"WTF Cinema bo'tiga xayriya ({amount} UZS)",
            "return_url": success_url or f"https://t.me/WTF_cinema_bot?start=payment_success_{transaction_id}",
            "cancel_url": cancel_url or f"https://t.me/WTF_cinema_bot?start=payment_cancel_{transaction_id}",
            "custom_fields": {
                "user_id": str(user_id)
            }
        }
        
        response = requests.post(STARS_PAYMENT_URL, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                return {
                    "success": True,
                    "payment_url": result["data"]["payment_url"],
                    "transaction_id": transaction_id
                }
            else:
                logger.error(f"Payment creation failed: {result.get('message')}")
                return {"success": False, "error": result.get("message")}
        else:
            logger.error(f"Payment API error: {response.status_code} - {response.text}")
            return {"success": False, "error": f"API error: {response.status_code}"}
    except Exception as e:
        logger.error(f"Exception in create_payment_link: {e}")
        return {"success": False, "error": str(e)}


@shared_task
def process_donation(donation_id):
    try:
        donation = Donation.objects.get(id=donation_id)
        user = donation.user
        
        activate(set_language_code(user.telegram_id))
        
        payment_result = create_payment_link(donation.amount, user.telegram_id)
        
        if payment_result["success"]:
            donation.transaction_id = payment_result["transaction_id"]
            donation.payment_url = payment_result["payment_url"]
            donation.save()
            
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                InlineKeyboardButton(text="💸 To'lovni amalga oshirish", url=payment_result["payment_url"])
            )
            
            bot.send_message(
                user.telegram_id,
                f"*WTF Cinema uchun {donation.amount} UZS xayriya*\n\n"
                f"To'lovni amalga oshirish uchun quyidagi tugmani bosing.",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
            
            return True
        else:
            donation.status = DonationStatus.FAILED
            donation.save()
            
            bot.send_message(
                user.telegram_id,
                f"*Xayriya to'lovini yaratishda xatolik yuz berdi*\n\n"
                f"Xatolik: {payment_result.get('error', 'Noma\'lum xatolik')}",
                parse_mode="Markdown"
            )
            
            return False
            
    except Donation.DoesNotExist:
        logger.error(f"Donation with ID {donation_id} does not exist")
        return False
    except Exception as e:
        logger.error(f"Error in process_donation: {e}")
        return False


@shared_task
def update_donation_status(transaction_id, status):
    try:
        donation = Donation.objects.get(transaction_id=transaction_id)
        
        if status == "success":
            donation.status = DonationStatus.COMPLETED
            donation.completed_at = datetime.now()
            donation.save()
            
            bot.send_message(
                donation.user.telegram_id,
                f"*Xayriyangiz uchun rahmat! ❤️*\n\n"
                f"Sizning {donation.amount} UZS xayriyangiz muvaffaqiyatli qabul qilindi.",
                parse_mode="Markdown"
            )
        elif status == "cancelled":
            donation.status = DonationStatus.CANCELLED
            donation.save()
            
            bot.send_message(
                donation.user.telegram_id,
                "*Xayriya bekor qilindi*\n\n"
                "Xayriya qilish uchun istagan vaqt urinib ko'rishingiz mumkin.",
                parse_mode="Markdown"
            )
        
        return True
    except Donation.DoesNotExist:
        logger.error(f"Donation with transaction_id {transaction_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error in update_donation_status: {e}")
        return False 