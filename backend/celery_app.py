# celery_app.py
from celery import Celery

celery_app = Celery(
    "reminder_app",
    broker="redis://localhost:6379/0",  # Redis URL
    backend="redis://localhost:6379/0",
)

celery_app.conf.timezone = "Asia/Kolkata"
from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
