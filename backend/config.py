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
    CELERY_TIMEZONE = "Asia/Kolkata"
    CELERY_ENABLE_UTC = False
    CELERY_BEAT_SCHEDULE = {
        "check-missed-medications-every-30-seconds": {
            "task": "tasks.check_missed_medications",
            "schedule": 30.0,
        },
        "send-daily-news-update-every-morning": {
            "task": "tasks.send_daily_news_update",
            "schedule": crontab(hour=9, minute=0),
        },
    }
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER", os.environ.get("MAIL_USERNAME")
    )

    # Sample ENV configuration for Flask-Mail
    # MAIL_SERVER = "smtp.gmail.com"
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = "your-email@gmail.com"
    # MAIL_PASSWORD = "16 digit app password to be generated from google account"
    # MAIL_DEFAULT_SENDER = "your-email@gmail.com"
