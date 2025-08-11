from config import Config


class TestConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    SECRET_KEY = "test-secret-key"
    JWT_SECRET_KEY = "test-jwt-secret"

    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True

    MAIL_SUPPRESS_SEND = True

    # Flask-Security configuration for testing
    SECURITY_PASSWORD_SALT = "test-security-salt"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
    WTF_CSRF_ENABLED = False
