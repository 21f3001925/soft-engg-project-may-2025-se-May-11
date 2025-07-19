from app import app
from celery_app import make_celery

# Configure the global celery_app instance with the Flask app context
celery_app = make_celery(app)
