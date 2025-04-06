import os
import sys

# Add the project root directory to the Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Initialize Django
import django
django.setup()

# Run the bot
from apps.bot.main import run
run() 