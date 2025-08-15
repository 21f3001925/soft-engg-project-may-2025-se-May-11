from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_current_user
from models import User, Role, db, Caregiver, SeniorCitizen, ServiceProvider

import bcrypt
from schemas.auth import (
    SignupSchema,
    LoginSchema,
    TokenSchema,
    MsgSchema,
    ChangePasswordSchema,
)


auth_blp = Blueprint(
    "Auth",
    "Auth",
    url_prefix="/api/v1/auth",
    description="This route handles user authentication, a critical component of the system. It allows different user types (seniors, caregivers, service providers) to sign up and log in securely. The signup endpoint creates new user accounts, while the login endpoint authenticates existing users and provides an access token for securing access to other parts of the application.",
)


@auth_blp.route("/signup")
class SignupResource(MethodView):
    @auth_blp.doc(
        summary="Create a new user account.",
        description="This endpoint allows a new user to create an account. The user can be a caregiver, a senior citizen, or a service provider. The user must provide an email or phone number, a password, and their role. Upon successful registration, the user is automatically logged in and an access token is returned.",
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

        # Create the role-specific model and associate it with the user
        if role_name == "senior_citizen":
            user.senior_citizen = SeniorCitizen()
        elif role_name == "caregiver":
            user.caregiver = Caregiver()
        elif role_name == "service_provider":
            user.service_provider = ServiceProvider()

        session.add(user)
        session.commit()

        access_token = create_access_token(identity=str(user.user_id))
        return {"access_token": access_token}, 201


@auth_blp.route("/login")
class LoginResource(MethodView):
    @auth_blp.doc(
        summary="Log in an existing user.",
        description="This endpoint allows an existing user to log in using their email or phone number and password. Upon successful authentication, an access token is returned, which can be used to access protected routes.",
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
            # Determine role by checking which table contains the user_id
            role = None
            if db.session.query(SeniorCitizen).filter_by(user_id=user.user_id).first():
                role = "senior_citizen"
            elif db.session.query(Caregiver).filter_by(user_id=user.user_id).first():
                role = "caregiver"
            elif (
                db.session.query(ServiceProvider)
                .filter_by(user_id=user.user_id)
                .first()
            ):
                role = "service_provider"
            else:
                role = "unknown"
            return {"access_token": access_token, "roles": [role]}, 200
        abort(401, message="Bad email or password")


@auth_blp.route("/change-password")
class ChangePasswordResource(MethodView):
    @auth_blp.doc(
        summary="Change the current user's password.",
        description="This endpoint allows a logged-in user to change their password. The user must provide their current password and a new password. This helps to keep the user's account secure.",
    )
    @auth_blp.arguments(ChangePasswordSchema())
    @auth_blp.response(200, MsgSchema())
    @auth_blp.alt_response(400, schema=MsgSchema())
    @auth_blp.alt_response(401, schema=MsgSchema())
    @jwt_required()
    def post(self, data):
        user_id = get_current_user().user_id
        user = db.session.query(User).filter_by(user_id=user_id).first()

        if not user:
            abort(401, message="User not found.")

        current_password = data["current_password"]
        new_password = data["new_password"]
        confirm_new_password = data["confirm_new_password"]

        if not bcrypt.checkpw(current_password.encode(), user.password.encode()):
            abort(401, message="Invalid current password.")

        if new_password != confirm_new_password:
            abort(400, message="New password and confirmation do not match.")

        if len(new_password) < 6:
            abort(400, message="New password must be at least 6 characters long.")

        user.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        db.session.commit()

        return {"msg": "Password changed successfully"}, 200
