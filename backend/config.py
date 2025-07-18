import os
from dotenv import load_dotenv
from celery.schedules import crontab

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-very-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///senior_citizen.db"
    )
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-very-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = "Senior Citizen API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/api/v1"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get(
        "GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET"
    )
    FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
    NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "")
    BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")
    API_SPEC_OPTIONS = {
        "servers": [{"url": BASE_URL}],
        "security": [{"jwt": []}],
        "components": {
            "securitySchemes": {
                "jwt": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
    }
    # Celery Configuration
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
    )
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TIMEZONE = "UTC"
    CELERY_ENABLE_UTC = True
    CELERY_BEAT_SCHEDULE = {
        "check-missed-medications-every-15-minutes": {
            "task": "backend.tasks.check_missed_medications",
            "schedule": 900.0,  # 15 minutes
        },
        "send-daily-news-update-every-morning": {
            "task": "backend.tasks.send_daily_news_update",
            "schedule": crontab(hour=9, minute=0),  # Every day at 9 AM UTC
        },
    }
