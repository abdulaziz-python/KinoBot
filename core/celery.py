import os

from celery import Celery

# from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Check if RabbitMQ is available
try:
    broker_url = os.getenv("CELERY_BROKER", f"amqp://{os.getenv('RABBITMQ_DEFAULT_USER')}:{os.getenv('RABBITMQ_DEFAULT_PASS')}@localhost:{os.getenv('AMQP_PORT', 5672)}//")
    backend_url = os.getenv("CELERY_RESULT_BACKEND", "db+mysql://{user}:{password}@{host}:{port}/{db}".format(
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        db=os.getenv("DATABASE_NAME").replace("$", "%24")  # Encode $ character
    ))
except Exception:
    # In case of error, fallback to database as broker (useful for PythonAnywhere)
    broker_url = "django://"
    backend_url = "db+mysql://{user}:{password}@{host}:{port}/{db}".format(
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
        db=os.getenv("DATABASE_NAME").replace("$", "%24")  # Encode $ character
    )

app = Celery("core", 
             broker=broker_url,
             backend=backend_url)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
