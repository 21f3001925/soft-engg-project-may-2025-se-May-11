from flask import Flask
from scheduler import start_scheduler
from db_session import Session
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from routes.auth import auth_blp
from routes.medications import medications_blp

app = Flask(__name__)

start_scheduler()

# SQLite DB URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///senior_citizen.db"
app.config["JWT_SECRET_KEY"] = "your-very-secret-key"
app.config["API_TITLE"] = "Senior Citizen API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/api/v1"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
jwt = JWTManager(app)

api.register_blueprint(auth_blp)
api.register_blueprint(medications_blp)


@app.route("/")
def hello_world():
    return "Hello, World! from Backend"


@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove()


if __name__ == "__main__":
    app.run(debug=True)
