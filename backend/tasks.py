import os
import sys
from datetime import datetime, timedelta
import requests

# --- Start of Fix ---
# This block ensures that the current directory (backend/) is in the Python path.
# This is crucial for the Celery worker, which might not have the correct path configured,
# causing ModuleNotFoundError for local modules like 'app_factory' or 'models'.
# We insert at the beginning of the path to prioritize our project's modules.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# --- End of Fix ---

from celery_app import celery_app
from extensions import socketio
from utils.notification import send_sms, send_email


# Lazy‐load Flask app factory to avoid circular imports
_flask_app = None


def get_flask_app():
    """
    Lazily creates and returns a Flask app instance.
    This avoids circular imports and ensures the app context is available
    only when the task is executed by a Celery worker.
    """
    global _flask_app
    if _flask_app is None:
        # Now that the path is corrected, we can use a standard absolute import.
        from app_factory import create_app

        _flask_app = create_app()
    return _flask_app


@celery_app.task
def send_reminder_notification(appointment_id, title, location, date_time, user_email):
    app = get_flask_app()
    with app.app_context():
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


@celery_app.task
def send_medication_reminder(medication_id):
    """
    Sends an SMS reminder for a specific medication.
    """
    app = get_flask_app()
    with app.app_context():
        # Models are imported here to ensure they are loaded within the app context
        from models import User, Medication

        med = Medication.query.get(medication_id)
        if med and not med.isTaken:
            user = User.query.get(med.senior_id)
            if user and user.phone_number:
                send_sms(
                    user.phone_number, f"Reminder: Take {med.dosage} of {med.name}"
                )
                print(f"Sent medication reminder to {user.username}")
            else:
                print(f"No user or phone for medication ID {medication_id}")
        else:
            print(f"Medication {medication_id} not found or already taken")


@celery_app.task
def send_event_reminder(user_id, event_name, event_location, event_time):
    app = get_flask_app()
    with app.app_context():
        from models import User

        user = User.query.get(user_id)
        if user and user.phone_number:
            send_sms(
                user.phone_number,
                f"Reminder: {event_name} at {event_location} on {event_time}",
            )


# @celery_app.task
# def send_daily_news_update(user_id):
#     app = get_flask_app()
#     with app.app_context():
#         from models import User

#         user = User.query.get(user_id)
#         if not user:
#             return

#         api_key = app.config.get("NEWSAPI_KEY")
#         if not api_key:
#             print("News API key not set")
#             return

#         try:
#             category = getattr(user.senior_citizen, "news_categories", None) or "general"
#             resp = requests.get(
#                 f"https://newsapi.org/v2/top-headlines?country=us"
#                 f"&category={category}&apiKey={api_key}"
#             )
#             resp.raise_for_status()
#             articles = resp.json().get("articles", [])[:5]

#             summary = "Your Daily News Update:\n\n" + "".join(
#                 f"- {a['title']} ({a['source']['name']})\n  Read more: {a['url']}\n\n"
#                 for a in articles
#             )
#             send_email(app, user.email, "Daily News Update", summary)
#         except Exception as e:
#             print(f"News fetch error for {user.username}: {e}")


@celery_app.task
def send_daily_news_update():
    """
    Fetches news updates for ALL users and sends them an email.
    This is designed to be run on a schedule by Celery Beat.
    """
    app = get_flask_app()
    with app.app_context():
        from models import User

        # Get all users from the database.
        # You could filter this further, e.g., for users who have opted-in.
        users_to_notify = User.query.all()
        print(f"Found {len(users_to_notify)} users for daily news update.")

        api_key = app.config.get("NEWSAPI_KEY")
        if not api_key:
            print("News API key not set, aborting daily news task.")
            return

        # Loop through each user and send them the news
        for user in users_to_notify:
            if not user.email:
                print(
                    f"Skipping user {user.username} (ID: {user.user_id}) - no email address."
                )
                continue

            try:
                # Default to 'general' news, but use user's preference if available.
                category = "general"
                if (
                    hasattr(user, "senior_citizen")
                    and user.senior_citizen
                    and getattr(user.senior_citizen, "news_categories", None)
                ):
                    category = user.senior_citizen.news_categories

                resp = requests.get(
                    f"https://newsapi.org/v2/top-headlines?country=us"
                    f"&category={category}&apiKey={api_key}"
                )
                resp.raise_for_status()  # Raise an exception for bad status codes
                articles = resp.json().get("articles", [])[:5]

                if not articles:
                    print(
                        f"No articles found for category '{category}' for user {user.username}."
                    )
                    continue

                summary = "Your Daily News Update:\n\n" + "".join(
                    f"- {a['title']} ({a['source']['name']})\n  Read more: {a['url']}\n\n"
                    for a in articles
                )
                send_email(app, user.email, "Daily News Update", summary)
                print(
                    f"Successfully sent daily news update to {user.username} at {user.email}"
                )

            except Exception as e:
                print(f"Failed to send news to {user.username}. Error: {e}")


@celery_app.task
def check_missed_medications():
    app = get_flask_app()
    with app.app_context():
        from models import User, Medication

        now = datetime.utcnow()
        cutoff = now - timedelta(hours=1)
        missed = Medication.query.filter(
            Medication.isTaken.is_(False), Medication.time <= cutoff
        ).all()

        for med in missed:
            senior = User.query.get(med.senior_id)
            if getattr(senior, "caregiver_id", None):
                caregiver = User.query.get(senior.caregiver_id)
                if caregiver and caregiver.phone_number:
                    msg = (
                        f"ALERT: {senior.username} missed {med.dosage} of "
                        f"{med.name} due at {med.time.strftime('%H:%M')}"
                    )
                    send_sms(caregiver.phone_number, msg)
                    send_email(app, caregiver.email, "Missed Medication Alert", msg)


@celery_app.task
def send_emergency_alert(senior_id):
    app = get_flask_app()
    with app.app_context():
        from models import User

        senior = User.query.get(senior_id)
        if not senior:
            return

        alert = f"EMERGENCY ALERT: {senior.username} pressed the emergency button!"
        # Caregiver
        cid = getattr(senior, "caregiver_id", None)
        if cid:
            care = User.query.get(cid)
            if care:
                if care.phone_number:
                    send_sms(care.phone_number, alert)
                send_email(app, care.email, "EMERGENCY ALERT!", alert)
        # Contacts
        for contact in getattr(senior, "emergency_contacts", []):
            if contact.phone:
                send_sms(contact.phone, alert)
            if contact.email:
                send_email(app, contact.email, "EMERGENCY ALERT!", alert)
