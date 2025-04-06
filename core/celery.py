import os

from celery import Celery

# from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core", 
             broker=os.getenv("CELERY_BROKER", f"amqp://{os.getenv('RABBITMQ_DEFAULT_USER')}:{os.getenv('RABBITMQ_DEFAULT_PASS')}@localhost:{os.getenv('AMQP_PORT', 5672)}//"),
             backend=os.getenv("CELERY_RESULT_BACKEND", "db+postgresql://{user}:{password}@{host}:{port}/{db}".format(
                 user=os.getenv("POSTGRES_USER"),
                 password=os.getenv("POSTGRES_PASSWORD"),
                 host=os.getenv("POSTGRES_BOUNCER_HOST"),
                 port=os.getenv("POSTGRES_BOUNCER_PORT"),
                 db=os.getenv("POSTGRES_DB")
             )))

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
