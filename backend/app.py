from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
from backend.db_session import Session
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# SQLite DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///senior_citizen.db'
app.config['JWT_SECRET_KEY'] = 'your-very-secret-key'

jwt = JWTManager(app)

@app.route("/")
def hello_world():
    return "Hello, World! from Backend"


@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove()


# Register Blueprints
from routes.api_v1 import api_v1
app.register_blueprint(api_v1)

if __name__ == "__main__":
    app.run(debug=True)
