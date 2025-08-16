from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_current_user
from models import db
from schemas.accessibility import AccessibilitySettingsSchema

accessibility_bp = Blueprint(
    "Accessibility",
    "Accessibility",
    url_prefix="/api/v1/accessibility",
    description="This blueprint provides endpoints for managing user accessibility settings, such as font size and theme. These settings are designed to make the application more user-friendly for senior citizens, allowing them to customize the interface to their specific needs.",
)


@accessibility_bp.route("")
class AccessibilitySettingsResource(MethodView):
    @jwt_required()
    @accessibility_bp.doc(
        summary="Get the current user's accessibility settings",
        description="This endpoint retrieves the current accessibility settings for the logged-in user. This includes the user's preferred font size and theme. These settings can be used to customize the user interface.",
    )
    @accessibility_bp.response(200, AccessibilitySettingsSchema)
    def get(self):
        user = get_current_user()
        return {
            "font_size": (
                user.senior_citizen.font_size if user.senior_citizen else "small"
            ),
            "theme": user.senior_citizen.theme if user.senior_citizen else "light",
        }

    @jwt_required()
    @accessibility_bp.doc(
        summary="Update the current user's accessibility settings",
        description="This endpoint allows the logged-in user to update their accessibility settings. The user can provide a new font size and/or theme. These settings will be saved and applied to the user interface.",
    )
    @accessibility_bp.arguments(AccessibilitySettingsSchema)
    @accessibility_bp.response(200, AccessibilitySettingsSchema)
    def put(self, update_data):
        user = get_current_user()
        if not user.senior_citizen:
            abort(400, message="User is not a senior citizen.")

        senior_citizen = user.senior_citizen
        if "font_size" in update_data:
            senior_citizen.font_size = update_data["font_size"]
        if "theme" in update_data:
            senior_citizen.theme = update_data["theme"]

        db.session.commit()

        return {
            "font_size": senior_citizen.font_size,
            "theme": senior_citizen.theme,
        }
