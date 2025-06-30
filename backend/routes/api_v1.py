from flask import Blueprint
from routes.medications import medications_bp
from routes.auth import auth_bp


api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Register feature blueprints on this parent blueprint
api_v1.register_blueprint(medications_bp)
api_v1.register_blueprint(auth_bp)

