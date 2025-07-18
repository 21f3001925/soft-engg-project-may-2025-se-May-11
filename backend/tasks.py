# tasks.py
from celery_app import celery_app
from extensions import socketio


@celery_app.task
def send_reminder_notification(appointment_id, title, location, date_time, user_email):
    print(f" Reminder: '{title}' at '{location}' on {date_time} (ID: {appointment_id})")
    print(f" Would send email to: {user_email}")

    # Emit real-time popup notification
    socketio.emit(
        "reminder",
        {
            "appointment_id": appointment_id,
            "title": title,
            "location": location,
            "date_time": date_time,
            "user_email": user_email,
        },
    )
