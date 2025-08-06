from app_factory import create_app
from extensions import socketio

# Create the Flask app instance for Gunicorn
app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)
