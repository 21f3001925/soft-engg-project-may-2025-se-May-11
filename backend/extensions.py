from flask_socketio import SocketIO
from flask_mail import Mail

socketio = SocketIO(message_queue="redis://localhost:6379/0", cors_allowed_origins="*")
mail = Mail()
