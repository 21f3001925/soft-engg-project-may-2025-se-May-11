from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from models import User
from db_session import Session
import bcrypt
from marshmallow import Schema, fields


class SignupSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class TokenSchema(Schema):
    access_token = fields.Str()


class MsgSchema(Schema):
    msg = fields.Str()


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
        session = Session()
        if (
            session.query(User)
            .filter((User.username == username) | (User.email == email))
            .first()
        ):
            session.close()
            abort(409, message="Username or email already exists")
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(username=username, email=email, password=hashed_pw)
        session.add(user)
        session.commit()
        access_token = create_access_token(identity=str(user.user_id))
        session.close()
        return {"access_token": access_token}, 201


@auth_blp.route("/login")
class LoginResource(MethodView):
    @auth_blp.arguments(LoginSchema())
    @auth_blp.response(200, TokenSchema())
    @auth_blp.alt_response(401, schema=MsgSchema())
    def post(self, data):
        username = data["username"]
        password = data["password"]
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        session.close()
        if (
            user
            and user.password
            and (
                bcrypt.checkpw(password.encode(), user.password.encode())
                if user.password.startswith("$2b$")
                else user.password == password
            )
        ):
            access_token = create_access_token(identity=str(user.user_id))
            return {"access_token": access_token}, 200
        abort(401, message="Bad username or password")
