from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_current_user
from models import db
from marshmallow import Schema, fields
import bcrypt
import os
from werkzeug.utils import secure_filename
from flask import request


class ProfileSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    name = fields.Str()
    avatar_url = fields.Str(dump_only=True)
    news_categories = fields.Str(allow_none=True)


class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True)


profile_bp = Blueprint(
    "Profile",
    "Profile",
    url_prefix="/api/v1/profile",
    description="This route allows users to manage their profile information, including their username, email, and password. It also provides functionality for users to upload an avatar and customize their experience, such as by selecting news preferences. This gives users control over their personal information and allows them to tailor the application to their needs.",
)


@profile_bp.route("")
class ProfileResource(MethodView):
    @jwt_required()
    @profile_bp.doc(summary="The current user can get their profile information")
    @profile_bp.response(200, ProfileSchema)
    def get(self):
        user = get_current_user()
        return user

    @jwt_required()
    @profile_bp.doc(summary="The current user can update their profile information")
    @profile_bp.arguments(ProfileSchema)
    @profile_bp.response(200, ProfileSchema)
    def put(self, update_data):
        user = get_current_user()
        for key, value in update_data.items():
            if key == "news_categories":
                if user.senior_citizen:
                    user.senior_citizen.news_categories = value
                else:
                    abort(400, message="User is not a senior citizen.")
            else:
                setattr(user, key, value)
        db.session.commit()
        return user

    @jwt_required()
    @profile_bp.doc(summary="The user can delete their profile if they want to.")
    @profile_bp.response(204)
    def delete(self):
        user = get_current_user()
        db.session.delete(user)
        db.session.commit()


@profile_bp.route("/change-password")
class ChangePasswordResource(MethodView):
    @jwt_required()
    @profile_bp.doc(
        summary="Users can change their password using this route to protect their accounts from security threats."
    )
    @profile_bp.arguments(ChangePasswordSchema)
    @profile_bp.response(204)
    def post(self, password_data):
        user = get_current_user()
        if not bcrypt.checkpw(
            password_data["current_password"].encode(), user.password.encode()
        ):
            abort(401, message="Invalid current password")
        user.password = bcrypt.hashpw(
            password_data["new_password"].encode(), bcrypt.gensalt()
        ).decode()
        db.session.commit()


@profile_bp.route("/avatar")
class AvatarUploadResource(MethodView):
    @jwt_required()
    @profile_bp.doc(
        summary="The user can upload their avatar using this route and change their avatar whenever required."
    )
    @profile_bp.response(200, ProfileSchema)
    def put(self):
        user = get_current_user()
        if "file" not in request.files:
            abort(400, message="No file part")
        file = request.files["file"]
        if file.filename == "":
            abort(400, message="No selected file")
        if file:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join("backend", "static", "uploads", "avatars")
            file.save(os.path.join(upload_folder, filename))
            user.avatar_url = f"/static/uploads/avatars/{filename}"
            db.session.commit()
        return user
