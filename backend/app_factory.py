from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_security import Security, SQLAlchemyUserDatastore, login_user
from flask_cors import CORS

# Core models and DB
from models import User, Role
from utils.jwt_flask_security_bridge import load_user_from_jwt
from utils.oauth_setup import init_oauth
from utils.add_roles import add_core_roles

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
from routes.caregiver_assignment import assignment_bp
from routes.accessibility import accessibility_bp
from routes.reports import reports_blp

from routes.chat import chat_blp

from config import Config

# Extensions
from extensions import db, socketio, mail

load_dotenv()


def create_app(config_class=None):
    """Application factory pattern"""
    app = Flask(__name__)

    # Use provided config class or default to Config
    if config_class is None:
        config_class = Config

    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)
    mail.init_app(app)
    jwt = JWTManager(app)

    CORS(
        app,
        origins="*",
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Security(app, user_datastore)

    api = Api(app)
    init_oauth(app)

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
    api.register_blueprint(assignment_bp)
    api.register_blueprint(accessibility_bp)
    api.register_blueprint(reports_blp)

    api.register_blueprint(chat_blp)

    with app.app_context():
        db.create_all()
        add_core_roles()

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        user = User.query.filter_by(user_id=identity).one_or_none()

        if user:
            login_user(user)
        return user

    app.before_request(load_user_from_jwt)

    @app.route("/")
    def hello_world():
        return "Hello, World! from Backend"

    # Serve static files (avatars)
    @app.route("/static/<path:filename>")
    def static_files(filename):
        return app.send_from_directory("static", filename)

    @app.teardown_appcontext
    def remove_session(exception=None):
        pass

    return app
