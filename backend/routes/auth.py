from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from models import User, Role, db, Caregiver, SeniorCitizen, ServiceProvider

import bcrypt
from schemas.auth import SignupSchema, LoginSchema, TokenSchema, MsgSchema

auth_blp = Blueprint("auth", "auth", url_prefix="/api/v1/auth")


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

        role_model_map = {
            "caregiver": Caregiver,
            "senior_citizen": SeniorCitizen,
            "service_provider": ServiceProvider,
        }
        model_class = role_model_map.get(role_name)
        if model_class:
            session.add(model_class(user_id=user.user_id))
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
