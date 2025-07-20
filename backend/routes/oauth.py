from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from models import User, Role, db
import os
from schemas.auth import TokenSchema, MsgSchema
from flask import redirect, url_for, current_app

oauth_blp = Blueprint(
    "OAuth", "OAuth", url_prefix="/api/v1/oauth", 
    description="As some users may prefer to login existing accounts, this route can be used to login with Google."
)


@oauth_blp.route("/google/login")
class GoogleOAuthLoginResource(MethodView):
    @oauth_blp.doc(summary="To login with Google id. New users will be registered automatically.")
    @oauth_blp.response(302)
    def get(self):
        redirect_uri = url_for("oauth.GoogleOAuthCallbackResource", _external=True)
        return current_app.oauth.google.authorize_redirect(redirect_uri)


@oauth_blp.route("/google/callback")
class GoogleOAuthCallbackResource(MethodView):
    @oauth_blp.doc(summary="Callback from Google OAuth")
    @oauth_blp.response(200, TokenSchema())
    @oauth_blp.alt_response(401, schema=MsgSchema())
    @oauth_blp.alt_response(400, schema=MsgSchema())
    def get(self):
        token = current_app.oauth.google.authorize_access_token()
        user_info = token.get("userinfo")
        if not user_info:
            abort(401, message="Failed to get user info from Google.")
        email = user_info.get("email")
        username = user_info.get("name")
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            role = db.session.query(Role).filter_by(name="caregiver").first()
            if not role:
                abort(400, message="Default role not found.")
            user = User(username=username, email=email, password=None)
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
        access_token = create_access_token(identity=str(user.user_id))
        frontend_url = os.environ.get(
            "FRONTEND_URL", "http://localhost:3000/oauth/callback"
        )
        redirect_url = f"{frontend_url}?token={access_token}"
        return redirect(redirect_url)
