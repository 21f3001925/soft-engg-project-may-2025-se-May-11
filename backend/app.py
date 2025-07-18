from backend.utils.oauth_setup import init_oauth
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS

# Core models and DB
from models import db, User, Role

# Core utilities and bridge
from utils.jwt_flask_security_bridge import load_user_from_jwt
from utils.add_roles import add_core_roles
from utils.scheduler import start_scheduler
from config import Config

# Blueprints
from routes.auth import auth_blp
from routes.oauth import oauth_blp
from routes.medications import medications_blp
from routes.providers import providers_bp
from routes.events import events_bp
from routes.profile import profile_bp
from routes.news import news_bp
from routes.reminder import reminder_blp
from routes.appointments import appointments_blp

# Extensions
from extensions import socketio

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

init_oauth(app)

start_scheduler()
db.init_app(app)


# Initialize socketio
socketio.init_app(app)
jwt = JWTManager(app)
CORS(app)
api = Api(app)

api.register_blueprint(auth_blp)
api.register_blueprint(oauth_blp)
api.register_blueprint(medications_blp)
api.register_blueprint(reminder_blp)
api.register_blueprint(appointments_blp)
api.register_blueprint(providers_bp)
api.register_blueprint(events_bp)
api.register_blueprint(profile_bp)
api.register_blueprint(news_bp)

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
