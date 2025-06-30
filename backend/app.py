from flask import Flask
from backend.db_session import Session
from flask_jwt_extended import JWTManager
from routes.api_v1 import api_v1

app = Flask(__name__)

# SQLite DB URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///senior_citizen.db"
app.config["JWT_SECRET_KEY"] = "your-very-secret-key"

jwt = JWTManager(app)

app.register_blueprint(api_v1)


@app.route("/")
def hello_world():
    return "Hello, World! from Backend"


@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove()


if __name__ == "__main__":
    app.run(debug=True)
