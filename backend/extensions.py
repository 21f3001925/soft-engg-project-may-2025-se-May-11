from flask_socketio import SocketIO

socketio = SocketIO(message_queue="redis://localhost:6379/0", cors_allowed_origins="*")
