from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from models import User, Role, db
import os

import bcrypt
from schemas.auth import SignupSchema, LoginSchema, TokenSchema, MsgSchema

from flask import redirect, url_for, current_app


auth_blp = Blueprint("auth", "auth", url_prefix="/api/v1/auth")


@auth_blp.route("/oauth/google/login")
class GoogleOAuthLoginResource(MethodView):
    @auth_blp.response(302)
    def get(self):
        redirect_uri = url_for("auth.GoogleOAuthCallbackResource", _external=True)
        return current_app.oauth.google.authorize_redirect(redirect_uri)


@auth_blp.route("/oauth/google/callback")
class GoogleOAuthCallbackResource(MethodView):
    @auth_blp.response(200, TokenSchema())
    @auth_blp.alt_response(401, schema=MsgSchema())
    @auth_blp.alt_response(400, schema=MsgSchema())
    def get(self):

        token = current_app.oauth.google.authorize_access_token()

        user_info = token.get("userinfo")
        if not user_info:
            abort(401, message="Failed to get user info from Google.")
        email = user_info.get("email")
        username = user_info.get("name")
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            # Assign default role, 'caregiver'
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


@auth_blp.route("/signup")
class SignupResource(MethodView):
    @auth_blp.arguments(SignupSchema())
    @auth_blp.response(201, TokenSchema())
    @auth_blp.alt_response(400, schema=MsgSchema())
    @auth_blp.alt_response(409, schema=MsgSchema())
    def post(self, data):
        username = data["username"]
        email = data["email"]
        password = data["password"]
        role_name = data["role"]
        session = db.session
        if (
            db.session.query(User)
            .filter((User.username == username) | (User.email == email))
            .first()
        ):

            abort(409, message="Username or email already exists")
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        role = db.session.query(Role).filter_by(name=role_name).first()
        if not role:

            abort(400, message="Invalid role specified")
        user = User(username=username, email=email, password=hashed_pw)
        user.roles.append(role)
        session.add(user)
        session.commit()
        access_token = create_access_token(identity=str(user.user_id))

        return {"access_token": access_token}, 201


@auth_blp.route("/login")
class LoginResource(MethodView):
    @auth_blp.arguments(LoginSchema())
    @auth_blp.response(200, TokenSchema())
    @auth_blp.alt_response(401, schema=MsgSchema())
    def post(self, data):
        username = data["username"]
        password = data["password"]
        user = db.session.query(User).filter_by(username=username).first()

        if (
            user
            and user.password
            and bcrypt.checkpw(password.encode(), user.password.encode())
        ):
            access_token = create_access_token(identity=str(user.user_id))
            return {"access_token": access_token}, 200
        abort(401, message="Bad username or password")
