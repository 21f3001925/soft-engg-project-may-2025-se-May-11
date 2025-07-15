# celery_app.py
from celery import Celery

celery_app = Celery(
    "reminder_app",
    broker="redis://localhost:6379/0",  # Redis URL
    backend="redis://localhost:6379/0"
)

celery_app.conf.timezone = 'Asia/Kolkata'
