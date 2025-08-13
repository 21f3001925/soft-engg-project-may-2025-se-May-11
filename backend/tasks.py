import os
import sys
from datetime import datetime, timedelta
import requests
import pytz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from celery_app import celery_app
from extensions import socketio
from utils.notification import send_sms, send_email


_flask_app = None


def get_flask_app():
    global _flask_app
    if _flask_app is None:
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
    """
    Sends an SMS and Email reminder for a specific event.
    """
    print(f"Event reminder task started for user {user_id}")
    app = get_flask_app()
    if app is None:
        print(f"Error: Flask app not initialized in Celery task for user {user_id}")
        return

    with app.app_context():
        try:
            from models import User

            print(f"Attempting to fetch user {user_id}")
            user = User.query.get(user_id)
            if not user:
                print(f"Event Reminder Task: User with ID {user_id} not found.")
                return

            print(f"User {user.username} found. Processing event reminder.")

            # --- IMPROVED: Better datetime formatting and timezone handling ---
            try:
                # Define IST timezone
                ist_tz = pytz.timezone("Asia/Kolkata")

                # Parse the event time (should be in IST ISO format)
                event_datetime_obj = datetime.fromisoformat(event_time)

                # Ensure it's in IST for display
                if event_datetime_obj.tzinfo:
                    event_datetime_obj = event_datetime_obj.astimezone(ist_tz)
                else:
                    # If for some reason it's naive, assume IST and localize
                    event_datetime_obj = ist_tz.localize(event_datetime_obj)

                # Format to a friendly string like "August 20, 2025 at 02:00 PM IST"
                formatted_time = event_datetime_obj.strftime(
                    "%B %d, %Y at %I:%M %p IST"
                )
                print(f"Successfully parsed and formatted event time: {formatted_time}")

            except (ValueError, TypeError) as e:
                # Fallback if the date format is unexpected
                print(f"Date parsing error: {e}")
                formatted_time = str(event_time)

            message = (
                f"🎉 Event Reminder: Your event '{event_name}' is scheduled at {event_location} "
                f"on {formatted_time}. Don't forget to attend!"
            )
            email_subject = f"Event Reminder: {event_name}"

            # Create HTML email content
            email_html = f"""
            <html>
            <body>
                <h2>🎉 Event Reminder</h2>
                <p>This is a friendly reminder about your upcoming event:</p>
                <ul>
                    <li><strong>Event:</strong> {event_name}</li>
                    <li><strong>Location:</strong> {event_location}</li>
                    <li><strong>Date & Time:</strong> {formatted_time}</li>
                </ul>
                <p>We look forward to seeing you there!</p>
            </body>
            </html>
            """

            # Send SMS if a phone number is available
            if user.phone_number:
                try:
                    print(
                        f"Attempting to send SMS to {user.username} ({user.phone_number})"
                    )
                    send_sms(user.phone_number, message)
                    print(
                        f"✅ Sent event SMS reminder to {user.username} ({user.phone_number})"
                    )
                except Exception as e:
                    print(f"❌ Failed to send SMS to {user.username}: {e}")

            # Send email if an email address is available
            if user.email:
                try:
                    print(f"Attempting to send email to {user.username} ({user.email})")
                    send_email(app, user.email, email_subject, email_html)
                    print(
                        f"✅ Sent event email reminder to {user.username} ({user.email})"
                    )
                except Exception as e:
                    print(f"❌ Failed to send email to {user.username}: {e}")

            print(f"Event reminder task completed for user {user_id}")

        except Exception as e:
            print(
                f"An unhandled error occurred in send_event_reminder for user {user_id}: {e}"
            )


@celery_app.task
def send_daily_news_update():
    app = get_flask_app()
    with app.app_context():
        from models import User

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
                resp.raise_for_status()
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
        from models import User, Medication, CaregiverAssignment, db

        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=10)
        missed_meds = Medication.query.filter(
            Medication.isTaken.is_(False), Medication.time <= cutoff
        ).all()

        for med in missed_meds:
            senior_user = User.query.get(med.senior_id)
            if not senior_user:
                continue

            # Increment medications_missed for the senior citizen
            if senior_user.senior_citizen:  # Check if the user is a senior citizen
                senior_user.senior_citizen.medications_missed += 1
                db.session.add(senior_user.senior_citizen)  # Add to session for update
                db.session.commit()  # Commit the change

            assignment = CaregiverAssignment.query.filter_by(
                senior_id=senior_user.user_id
            ).first()
            if assignment:
                caregiver_user = User.query.get(assignment.caregiver_id)
                if caregiver_user:
                    msg = (
                        f"ALERT: {senior_user.name} may have missed their dose of "
                        f"{med.dosage} of {med.name}, which was due at "
                        f"{med.time.strftime('%I:%M %p')}. Medications missed count: {senior_user.senior_citizen.medications_missed if senior_user.senior_citizen else 'N/A'}."
                    )
                    if caregiver_user.phone_number:
                        send_sms(caregiver_user.phone_number, msg)
                    send_email(
                        app, caregiver_user.email, "Missed Medication Alert", msg
                    )


@celery_app.task
def send_emergency_alert(senior_id):
    app = get_flask_app()
    with app.app_context():
        from models import User, CaregiverAssignment

        senior_user = User.query.get(senior_id)
        if not senior_user:
            return

        alert_msg = f"EMERGENCY ALERT: {senior_user.name} has triggered an emergency alert. Please check on them immediately."

        assignment = CaregiverAssignment.query.filter_by(
            senior_id=senior_user.user_id
        ).first()
        if assignment:
            caregiver_user = User.query.get(assignment.caregiver_id)
            if caregiver_user:
                print(f"Notifying assigned caregiver: {caregiver_user.name}")
                if caregiver_user.phone_number:
                    send_sms(caregiver_user.phone_number, alert_msg)
                send_email(app, caregiver_user.email, "EMERGENCY ALERT!", alert_msg)

        for contact in getattr(senior_user, "emergency_contacts", []):
            print(f"Notifying emergency contact: {contact.name}")
            if contact.phone:
                send_sms(contact.phone, alert_msg)
            if contact.email:
                send_email(app, contact.email, "EMERGENCY ALERT!", alert_msg)
