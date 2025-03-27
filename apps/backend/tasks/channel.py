import logging
import os
import re
import time

import telebot
from celery import shared_task
from django.utils.translation import gettext as _
from telebot import TeleBot

from apps.backend.models.channel import Channel, ChannelType
from apps.backend.models.cinema import Cinema

# Logger
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(TOKEN)





@shared_task
def process_channel_task(channel_id: int) -> None:...