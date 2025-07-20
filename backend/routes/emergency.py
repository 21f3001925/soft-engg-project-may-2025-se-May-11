from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from tasks import send_emergency_alert
from models import User

emergency_blp = Blueprint(
    "Emergency",
    "Emergency",
    url_prefix="/api/v1/emergency",
    description="This route performs the emergency alert operation for senior citizens. Upon pressing the emergency button, the system will alert the caregivers.",
)


@emergency_blp.route("/trigger")
class EmergencyTrigger(MethodView):
    @jwt_required()
    @emergency_blp.doc(summary="When the senior citizen presses the emergency button, the system will trigger alert to the caregivers which will help them attend to the needs of senior citizen.")
    @emergency_blp.response(200, description="Emergency alert triggered successfully")
    def post(self):
        user_id = get_jwt_identity()
        senior = User.query.get(user_id)

        if not senior or senior.roles[0].name != "senior_citizen":
            abort(403, message="Only senior citizens can trigger emergency alerts.")

        send_emergency_alert.delay(user_id)
        return {"message": "Emergency alert triggered"}, 200
