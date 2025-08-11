from flask import Flask
from app_factory import create_app
from extensions import socketio

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World! from Backend"


# Create the Flask app instance for Gunicorn
app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)
