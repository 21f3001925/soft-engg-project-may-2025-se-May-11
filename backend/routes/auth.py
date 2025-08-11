from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from models import User, Role, db, Caregiver, SeniorCitizen, ServiceProvider

import bcrypt
from schemas.auth import SignupSchema, LoginSchema, TokenSchema, MsgSchema

auth_blp = Blueprint(
    "Auth",
    "Auth",
    url_prefix="/api/v1/auth",
    description="This route handles user authentication, a critical component of the system. It allows different user types (seniors, caregivers, service providers) to sign up and log in securely. The signup endpoint creates new user accounts, while the login endpoint authenticates existing users and provides an access token for securing access to other parts of the application.",
)


@auth_blp.route("/signup")
class SignupResource(MethodView):
    @auth_blp.doc(
        summary="This route creates a new user. A user can be a caregiver, senior citizen or service provider. They can sign up using this route.",
    )
    @auth_blp.arguments(SignupSchema())
    @auth_blp.response(201, TokenSchema())
    @auth_blp.alt_response(400, schema=MsgSchema())
    @auth_blp.alt_response(409, schema=MsgSchema())
    def post(self, data):
        # Either email or phone_number must be provided
        email = data.get("email")
        password = data["password"]
        role_name = data["role"]
        phone_number = data.get("phone_number")
        session = db.session

        if not email and not phone_number:
            abort(400, message="Either email or phone number is required")
        if email and db.session.query(User).filter(User.email == email).first():
            abort(409, message="Email already exists")
        if (
            phone_number
            and db.session.query(User).filter(User.phone_number == phone_number).first()
        ):
            abort(409, message="Phone number already exists")
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        role = db.session.query(Role).filter_by(name=role_name).first()
        if not role:
            abort(400, message="Invalid role specified")

        # Generate a unique username server-side
        base_username = email.split("@")[0] if email else f"user_{phone_number}"
        candidate = base_username
        suffix = 1
        while db.session.query(User).filter_by(username=candidate).first():
            candidate = f"{base_username}{suffix}"
            suffix += 1

        user = User(
            username=candidate,
            email=email,
            password=hashed_pw,
            phone_number=phone_number,
        )
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
    @auth_blp.doc(
        summary="This route allows a user to log in using their username and password. They will get an access token in return."
    )
    @auth_blp.arguments(LoginSchema())
    @auth_blp.response(200, TokenSchema())
    @auth_blp.alt_response(401, schema=MsgSchema())
    def post(self, data):
        # Accept email OR phone
        password = data["password"]
        user = None
        if data.get("email"):
            user = db.session.query(User).filter_by(email=data["email"]).first()
        elif data.get("phone_number"):
            user = (
                db.session.query(User)
                .filter_by(phone_number=data["phone_number"])
                .first()
            )

        if (
            user
            and user.password
            and bcrypt.checkpw(password.encode(), user.password.encode())
        ):
            access_token = create_access_token(identity=str(user.user_id))
            return {"access_token": access_token}, 200
        abort(401, message="Bad email or password")
