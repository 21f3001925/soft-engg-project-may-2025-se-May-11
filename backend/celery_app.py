from celery import Celery
from config import Config


def create_celery():
    """Create and configure Celery instance"""
    celery = Celery(
        "senior_app",
        broker=Config.CELERY_BROKER_URL,
        backend=Config.CELERY_RESULT_BACKEND,
        include=[
            "tasks",
        ],  # Import tasks module
    )

    # Update configuration
    celery.conf.update(
        task_serializer=Config.CELERY_TASK_SERIALIZER,
        accept_content=Config.CELERY_ACCEPT_CONTENT,
        result_serializer=Config.CELERY_RESULT_SERIALIZER,
        timezone=Config.CELERY_TIMEZONE,
        enable_utc=Config.CELERY_ENABLE_UTC,
        beat_schedule=Config.CELERY_BEAT_SCHEDULE,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30 minutes
        task_soft_time_limit=60,  # 1 minute
        worker_prefetch_multiplier=1,
        task_acks_late=True,
    )

    return celery


# Create the Celery instance
celery_app = create_celery()
