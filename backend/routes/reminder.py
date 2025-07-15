# routes/reminder.py
from flask import Blueprint, request, jsonify
from tasks import send_reminder_notification
from datetime import datetime, timedelta

reminder_blp = Blueprint("reminder", __name__)

@reminder_blp.route("/api/schedule-reminder", methods=["POST"])
def schedule_reminder():
    data = request.get_json()
    appointment_id = data.get("appointment_id")
    title = data.get("title")
    location = data.get("location")
    date_time = data.get("date_time")
    user_email = data.get("email")

    if not all([appointment_id, title, location, date_time, user_email]):
        return jsonify({"error": "Missing required fields"}), 400

    time_formats = [1440, 60, 30, 10]  # Minutes before appointment
    date_time_obj = datetime.fromisoformat(date_time)

    for mins in time_formats:
        eta = date_time_obj - timedelta(minutes=mins)
        if eta > datetime.now():
            send_reminder_notification.apply_async(
                args=[appointment_id, title, location, date_time, user_email],
                eta=eta
            )

    # Final reminder at exact time
    if date_time_obj > datetime.now():
        send_reminder_notification.apply_async(
            args=[appointment_id, title, location, date_time, user_email],
            eta=date_time_obj
        )

    return jsonify({"message": "Reminders scheduled"}), 200
