# any configuration should be stored here
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))

TOKEN = os.getenv("BOT_TOKEN")
