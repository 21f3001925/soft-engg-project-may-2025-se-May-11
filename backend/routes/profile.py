from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_current_user
from models import db, User
import bcrypt
import os
from werkzeug.utils import secure_filename
from flask import current_app
from schemas.profile import (
    ProfileSchema,
    ChangePasswordSchema,
    AvatarUploadSchema,
    SeniorSchema,
)


profile_bp = Blueprint(
    "Profile",
    "Profile",
    url_prefix="/api/v1/profile",
    description="This route allows users to manage their profile information, including their username, email, and password. It also provides functionality for users to upload an avatar and customize their experience, such as by selecting news preferences. This gives users control over their personal information and allows them to tailor the application to their needs.",
)


@profile_bp.route("")
class ProfileResource(MethodView):
    @jwt_required()
    @profile_bp.doc(
        summary="Get the current user's profile information.",
        description="This endpoint returns the profile information of the currently logged-in user. This includes the user's username, email, and other personal details. This is useful for displaying the user's profile information in the application.",
    )
    @profile_bp.response(200, ProfileSchema)
    def get(self):
        user = get_current_user()
        return user

    @jwt_required()
    @profile_bp.doc(
        summary="Update the current user's profile information.",
        description="This endpoint allows the currently logged-in user to update their profile information. The user can update their username, email, and other personal details. This gives users control over their personal information and allows them to keep it up-to-date.",
    )
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
    @profile_bp.doc(
        summary="Delete the current user's profile.",
        description="This endpoint allows the currently logged-in user to delete their profile. This is a permanent action and cannot be undone. This gives users control over their personal information and allows them to remove it from the application if they wish.",
    )
    @profile_bp.response(204)
    def delete(self):
        user = get_current_user()
        db.session.delete(user)
        db.session.commit()


@profile_bp.route("/change-password")
class ChangePasswordResource(MethodView):
    @jwt_required()
    @profile_bp.doc(
        summary="Change the current user's password.",
        description="This endpoint allows the currently logged-in user to change their password. The user must provide their current password and a new password. This helps to keep the user's account secure.",
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
        summary="Upload or update the current user's avatar.",
        description="This endpoint allows the currently logged-in user to upload an avatar or update their existing one. The user must provide an image file. This allows users to personalize their profile and make it more recognizable.",
    )
    @profile_bp.arguments(AvatarUploadSchema, location="files")
    @profile_bp.response(200, ProfileSchema)
    def put(self, files):
        user = get_current_user()
        if "file" not in files:
            abort(400, message="No file part")
        file = files["file"]
        if file.filename == "":
            abort(400, message="No selected file")
        if file:
            filename = secure_filename(file.filename)
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            avatar_folder = os.path.join(upload_folder, "avatars")
            os.makedirs(avatar_folder, exist_ok=True)
            file.save(os.path.join(avatar_folder, filename))
            timestamp = datetime.now().timestamp()
            user.avatar_url = f"static/uploads/avatars/{filename}?t={timestamp}"
            db.session.commit()
        return user


@profile_bp.route("/caregiver/seniors")
class CaregiverSeniorsResource(MethodView):
    @jwt_required()
    @profile_bp.doc(
        summary="Get the list of seniors assigned to the current caregiver.",
        description="This endpoint returns a list of all seniors who are currently assigned to the logged-in caregiver. This allows caregivers to easily view the seniors they are responsible for and manage their care.",
    )
    @profile_bp.response(200, SeniorSchema(many=True))
    def get(self):
        user = User.query.get("007b3fe8-6e33-4317-896d-88d5a651061a")
        if not user.caregiver:
            abort(403, message="User is not a caregiver")

        seniors = [assignment.senior.user for assignment in user.caregiver.assignments]
        return seniors
