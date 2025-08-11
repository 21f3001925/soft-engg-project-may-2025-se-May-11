from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_current_user
from models import db
from schemas.accessibility import AccessibilitySettingsSchema

accessibility_bp = Blueprint(
    "Accessibility",
    "Accessibility",
    url_prefix="/api/v1/accessibility",
    description="Operations for managing user accessibility settings (font size, theme).",
)


@accessibility_bp.route("")
class AccessibilitySettingsResource(MethodView):
    @jwt_required()
    @accessibility_bp.doc(summary="Get the current user's accessibility settings")
    @accessibility_bp.response(200, AccessibilitySettingsSchema)
    def get(self):
        user = get_current_user()
        if not user.senior_citizen:
            abort(400, message="User is not a senior citizen.")

        print(
            f"GET accessibility settings for user {user.user_id}: font_size={user.senior_citizen.font_size}, theme={user.senior_citizen.theme}"
        )
        return {
            "font_size": user.senior_citizen.font_size,
            "theme": user.senior_citizen.theme,
        }

    @jwt_required()
    @accessibility_bp.doc(summary="Update the current user's accessibility settings")
    @accessibility_bp.arguments(AccessibilitySettingsSchema)
    @accessibility_bp.response(200, AccessibilitySettingsSchema)
    def put(self, update_data):
        user = get_current_user()
        if not user.senior_citizen:
            abort(400, message="User is not a senior citizen.")

        print(
            f"PUT accessibility settings received for user {user.user_id}: {update_data}"
        )
        senior_citizen = user.senior_citizen
        if "font_size" in update_data:
            senior_citizen.font_size = update_data["font_size"]
        if "theme" in update_data:
            senior_citizen.theme = update_data["theme"]

        db.session.commit()
        print(
            f"PUT accessibility settings committed for user {user.user_id}: font_size={senior_citizen.font_size}, theme={senior_citizen.theme}"
        )

        return {
            "font_size": senior_citizen.font_size,
            "theme": senior_citizen.theme,
        }
