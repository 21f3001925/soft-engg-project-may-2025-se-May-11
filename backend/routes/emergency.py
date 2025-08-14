from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from tasks import send_emergency_alert
from models import User
from marshmallow import Schema, fields
from flask import request

emergency_blp = Blueprint(
    "Emergency",
    "Emergency",
    url_prefix="/api/v1/emergency",
    description="This route handles the emergency alert system. When a senior citizen triggers an alert, this API is responsible for notifying their registered caregivers and emergency contacts. This provides a quick and effective way for seniors to request help, ensuring their safety and providing peace of mind for their loved ones.",
)


# --- 1. ADD A SCHEMA FOR THE INCOMING LOCATION DATA ---
class EmergencyTriggerSchema(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)


@emergency_blp.route("/trigger")
class EmergencyTrigger(MethodView):
    @jwt_required()
    @emergency_blp.doc(
        summary="When the senior citizen presses the emergency button, the system will trigger alert to the caregivers which will help them attend to the needs of senior citizen."
    )
    @emergency_blp.response(200, description="Emergency alert triggered successfully")
    def post(self):
        user_id = get_jwt_identity()
        senior = User.query.get(user_id)

        if not senior or "senior_citizen" not in [role.name for role in senior.roles]:
            abort(403, message="Only senior citizens can trigger emergency alerts.")

        # --- 4. MANUALLY and SAFELY get the JSON data from the request ---
        # This will be an empty dictionary {} if no data is sent.
        location_data = request.get_json(silent=True) or {}

        latitude = location_data.get("latitude")
        longitude = location_data.get("longitude")

        # Pass the data (or None) to the Celery task
        send_emergency_alert.delay(user_id, latitude, longitude)

        if latitude and longitude:
            return {"message": "Emergency alert with location triggered"}
        else:
            return {"message": "Generic emergency alert triggered"}
