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
from utils.oauth_setup import init_oauth
from config import Config

# Blueprints
from routes.auth import auth_blp
from routes.oauth import oauth_blp
from routes.medications import medications_blp
from routes.providers import providers_bp
from routes.events import events_bp
from routes.profile import profile_bp
from routes.news import news_bp
from routes.emergency_contacts import emergency_contacts_blp
from routes.reminder import reminder_blp
from routes.appointments import appointments_blp
from routes.emergency import emergency_blp

# Extensions
from extensions import socketio
from celery_app import make_celery

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
init_oauth(app)
celery = make_celery(app)
db.init_app(app)
socketio.init_app(app)
jwt = JWTManager(app)
CORS(app)
api = Api(app)

# Register blueprints
api.register_blueprint(auth_blp)
api.register_blueprint(oauth_blp)
api.register_blueprint(medications_blp)
api.register_blueprint(reminder_blp)
api.register_blueprint(appointments_blp)
api.register_blueprint(providers_bp)
api.register_blueprint(events_bp)
api.register_blueprint(profile_bp)
api.register_blueprint(news_bp)
api.register_blueprint(emergency_contacts_blp)
api.register_blueprint(emergency_blp)

# Flask-Security
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
