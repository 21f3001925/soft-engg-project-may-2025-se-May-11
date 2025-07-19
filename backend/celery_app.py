# backend/celery_app.py

from celery import Celery
from config import Config

celery_app = Celery(
    "senior_app",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
    include=["backend.tasks"],  # fully qualified import path
)


def make_celery(app):
    celery_app.conf.update(app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app
