# routes/reminder.py

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from schemas.reminder import ReminderSchema, MsgSchema  # you’ll define this schema
from tasks import send_reminder_notification
from datetime import datetime, timedelta, timezone

reminder_blp = Blueprint(
    "Reminder",
    "Reminder",
    url_prefix="/api/v1/reminder",
    description="This route is used to schedule and send reminders for appointments and other events. It allows users to set up multiple reminders, ensuring they receive timely notifications. This is a critical feature for helping seniors remember important events, which is essential for their health and well-being, and can be customized to meet individual needs.",
)


@reminder_blp.route("/schedule-reminder")
class ReminderResource(MethodView):
    @jwt_required()
    @reminder_blp.doc(
        summary="Schedule reminders for an appointment.",
        description="This endpoint schedules a series of reminders for an appointment. Reminders are sent at various intervals before the appointment time (e.g., 24 hours, 1 hour, 30 minutes, and 10 minutes before). This helps to ensure that the user does not forget their appointment.",
    )
    @reminder_blp.arguments(ReminderSchema())
    @reminder_blp.response(200, MsgSchema())
    @reminder_blp.alt_response(400, schema=MsgSchema())
    def post(self, data):
        appointment_id = data.get("appointment_id")
        title = data.get("title")
        location = data.get("location")
        date_time = data.get("date_time")
        user_email = data.get("email")

        try:
            date_time_obj = datetime.fromisoformat(date_time)
        except Exception:
            abort(400, message="Invalid date_time format")

        time_formats = [1440, 60, 30, 10]  # Minutes before appointment

        for mins in time_formats:
            eta = date_time_obj - timedelta(minutes=mins)
            if eta > datetime.now(timezone.utc):
                send_reminder_notification.apply_async(
                    args=[appointment_id, title, location, date_time, user_email],
                    eta=eta,
                )

        # Final reminder at exact time
        if date_time_obj > datetime.now(timezone.utc):
            send_reminder_notification.apply_async(
                args=[appointment_id, title, location, date_time, user_email],
                eta=date_time_obj,
            )

        return {"message": "Reminders scheduled"}, 200
