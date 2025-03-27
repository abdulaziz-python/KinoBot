FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r /app/requirements.txt

ENV DJANGO_SETTINGS_MODULE=core.settings

ENV PYTHONPATH=/app

CMD ["python", "apps/bot/main.py"]