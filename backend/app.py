from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
from routes.auth import auth_blp

# from routes.appointments import appointments_bp # Uncomment when needed.
from routes.medications import medications_blp
from routes.providers import providers_bp
from routes.events import events_bp
from routes.profile import profile_bp
from routes.news import news_bp
from utils.scheduler import start_scheduler
from utils.oauth_setup import init_oauth
from utils.add_roles import add_core_roles
from utils.jwt_flask_security_bridge import load_user_from_jwt
from config import Config
from models import db, User, Role

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

init_oauth(app)

start_scheduler()
db.init_app(app)

jwt = JWTManager(app)
CORS(app)
api = Api(app)

api.register_blueprint(auth_blp)
# api.register_blueprint(appointments_bp) # Commented out because it's causing errors to run the server, once it's fixed uncomment this.
api.register_blueprint(medications_blp)
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
    app.run(debug=True)
