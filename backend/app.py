from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_security import Security, SQLAlchemyUserDatastore
from models import db, User, Role
from scheduler import start_scheduler
from add_roles import add_core_roles
from jwt_flask_security_bridge import load_user_from_jwt
from routes.reminder import reminder_blp
from extensions import socketio
import pyttsx3
from appointment import appointment_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-very-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///senior_citizen.db"
app.config["JWT_SECRET_KEY"] = "your-very-secret-key"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["API_TITLE"] = "Senior Citizen API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/api/v1"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

start_scheduler()
db.init_app(app)

# Initialize socketio
socketio.init_app(app)

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

api = Api(app)
jwt = JWTManager(app)

app.register_blueprint(reminder_blp)
app.register_blueprint(appointment_bp)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

with app.app_context():
    db.create_all()
    add_core_roles()

app.before_request(load_user_from_jwt)

@app.route("/")
def hello_world():
    return "Hello, World! from Backend"

@app.teardown_appcontext
def remove_session(exception=None):
    pass

if __name__ == "__main__":
    socketio.run(app, debug=True)
