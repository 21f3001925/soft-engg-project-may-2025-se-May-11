import os
import sys
from datetime import datetime, timedelta
import requests
import pytz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from celery_app import celery_app
from extensions import socketio
from utils.notification import send_sms, send_email
from models import User, Appointment, CaregiverAssignment, db


_flask_app = None


def get_flask_app():
    global _flask_app
    if _flask_app is None:
        from app_factory import create_app

        _flask_app = create_app()
    return _flask_app


@celery_app.task
def send_reminder_notification(appointment_id, title, location, date_time, user_email):
    """
    Sends a reminder via Socket.IO, Email, and SMS for a specific appointment.
    """
    app = get_flask_app()
    with app.app_context():
        from models import User

        # --- 1. Find the User ---
        user = User.query.filter_by(email=user_email).first()
        if not user:
            print(f"Appointment Reminder Task: User with email {user_email} not found.")
            return

        # --- 2. Create the Reminder Message ---
        try:
            # Format the date and time for the message
            event_datetime_obj = datetime.fromisoformat(date_time)
            formatted_time = event_datetime_obj.strftime("%B %d, %Y at %I:%M %p")
        except ValueError:
            formatted_time = date_time  # Fallback to the raw string

        message = (
            f"Appointment Reminder: Your appointment '{title}' at {location} "
            f"is scheduled for {formatted_time}."
        )
        email_subject = f"Reminder: {title}"

        # --- 3. Send Email and SMS ---
        if user.phone_number:
            send_sms(user.phone_number, message)
            print(f"✅ Sent appointment SMS reminder to {user.username}")

        if user.email:
            send_email(app, user.email, email_subject, message)
            print(f"✅ Sent appointment email reminder to {user.username}")

        # --- 4. Keep the original real-time notification ---
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
    Sends a reminder to the senior and a notification to the caregiver
    when a medication is due.
    """
    app = get_flask_app()
    with app.app_context():
        from models import User, Medication, CaregiverAssignment

        med = Medication.query.get(medication_id)
        if not med or med.isTaken:
            print(
                f"Medication reminder for {medication_id} skipped (not found or already taken)."
            )
            return

        senior_user = User.query.get(med.senior_id)
        if not senior_user:
            # Added clearer logging
            print(f"Task failed: User not found for medication ID {medication_id}.")
            return

        print(f"User '{senior_user.username}' found. Preparing reminders.")

        # --- 1. Reminder for the Senior (Corrected Logic) ---
        senior_msg = f"Reminder: It's time to take {med.dosage} of {med.name}."

        # Check for phone number and send SMS if it exists
        if senior_user.phone_number:
            send_sms(senior_user.phone_number, senior_msg)
            print(f"Sent SMS reminder to senior {senior_user.username}")
        else:
            print(f"Senior {senior_user.username} has no phone number. Skipping SMS.")

        # Check for email and send if it exists
        if senior_user.email:
            send_email(app, senior_user.email, "Medication Reminder", senior_msg)
            print(f"Sent email reminder to senior {senior_user.username}")
        else:
            print(f"Senior {senior_user.username} has no email. Skipping email.")

        # --- 2. Notification for the Caregiver (Logic is good, added logging) ---
        assignment = CaregiverAssignment.query.filter_by(
            senior_id=senior_user.user_id
        ).first()
        if assignment and (caregiver_user := User.query.get(assignment.caregiver_id)):
            print(
                f"Caregiver '{caregiver_user.username}' found. Preparing notification."
            )
            caregiver_msg = (
                f"Medication Due: It's time for {senior_user.name} to take "
                f"{med.dosage} of {med.name}. Please ensure it is marked as taken."
            )
            email_subject = f"Medication Due for {senior_user.name}"

            if caregiver_user.phone_number:
                send_sms(caregiver_user.phone_number, caregiver_msg)
                print(f"Sent SMS notification to caregiver {caregiver_user.username}")
            if caregiver_user.email:
                send_email(app, caregiver_user.email, email_subject, caregiver_msg)
                print(f"Sent email notification to caregiver {caregiver_user.username}")


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

        print("Running 'check_missed_medications' task...")
        now = datetime.now()
        cutoff = now - timedelta(minutes=10)

        missed_meds = Medication.query.filter(
            Medication.isTaken.is_(False),
            Medication.time <= cutoff,
            Medication.missed_counted.is_(False),
        ).all()

        if not missed_meds:
            print("No missed medications found.")
            return

        print(
            f"Found {len(missed_meds)} missed medication(s). Processing notifications..."
        )

        for med in missed_meds:
            senior_user = User.query.get(med.senior_id)
            if not senior_user:
                continue

            if senior_user.senior_citizen:
                senior_user.senior_citizen.medications_missed = (
                    senior_user.senior_citizen.medications_missed or 0
                ) + 1
                db.session.add(senior_user.senior_citizen)
                print(
                    f"Incremented missed counter for {senior_user.username} - medication: {med.name}"
                )

                med.missed_counted = True
                db.session.add(med)
                print(f"Marked {med.name} as counted to prevent double-counting")

            # --- NEW: Notify the Senior Citizen Directly ---
            senior_msg = (
                f"ALERT: You may have missed your dose of {med.dosage} of {med.name}, "
                f"which was due at {med.time.strftime('%I:%M %p')}. Please check your schedule."
            )
            if senior_user.phone_number:
                send_sms(senior_user.phone_number, senior_msg)
                print(f"Sent missed medication SMS to senior {senior_user.username}")
            if senior_user.email:
                send_email(
                    app, senior_user.email, "Missed Medication Alert", senior_msg
                )
                print(f"Sent missed medication email to senior {senior_user.username}")

            # --- EXISTING: Notify the Caregiver (if they exist) ---
            assignment = CaregiverAssignment.query.filter_by(
                senior_id=senior_user.user_id
            ).first()
            if assignment:
                caregiver_user = User.query.get(assignment.caregiver_id)
                if caregiver_user:
                    print(
                        f"Found caregiver '{caregiver_user.username}' for senior '{senior_user.username}'."
                    )
                    missed_count = (
                        senior_user.senior_citizen.medications_missed
                        if senior_user.senior_citizen
                        else "N/A"
                    )
                    caregiver_msg = (
                        f"ALERT: {senior_user.name} may have missed their dose of "
                        f"{med.dosage} of {med.name}, which was due at "
                        f"{med.time.strftime('%I:%M %p')}. "
                        f"Total medications missed: {missed_count}."
                    )

                    if caregiver_user.phone_number:
                        send_sms(caregiver_user.phone_number, caregiver_msg)
                        print(
                            f"Sent missed medication SMS to caregiver {caregiver_user.username}"
                        )
                    if caregiver_user.email:
                        send_email(
                            app,
                            caregiver_user.email,
                            "Missed Medication Alert",
                            caregiver_msg,
                        )
                        print(
                            f"Sent missed medication email to caregiver {caregiver_user.username}"
                        )

        db.session.commit()


@celery_app.task
def check_missed_appointments():
    """
    Checks for past appointments that were not marked as 'Completed' or 'Cancelled',
    updates the status to 'Missed', and sends a notification to the senior and caregiver.
    """
    app = get_flask_app()
    with app.app_context():

        now = datetime.now(pytz.utc)

        missed_appointments = Appointment.query.filter(
            Appointment.date_time <= now, Appointment.status == "Scheduled"
        ).all()

        if not missed_appointments:
            return

        print(f"Found {len(missed_appointments)} missed appointment(s). Processing...")

        for appt in missed_appointments:
            senior_user = User.query.get(appt.senior_id)

            if not senior_user or not senior_user.senior_citizen:
                continue

            # Increment Counter
            senior_user.senior_citizen.appointments_missed = (
                senior_user.senior_citizen.appointments_missed or 0
            ) + 1
            appt.status = "Missed"
            print("Successfully incremented missed counter and set status to 'Missed'.")

            # 1. Notify the Senior Citizen
            formatted_time = appt.date_time.astimezone(
                pytz.timezone("Asia/Kolkata")
            ).strftime("%B %d at %I:%M %p")
            senior_msg = (
                f"ALERT: It appears you missed your appointment for '{appt.title}' "
                f"that was scheduled for {formatted_time}. Please reschedule if necessary."
            )

            if senior_user.phone_number:
                print("Senior has a phone number. Attempting to send SMS.")
                send_sms(senior_user.phone_number, senior_msg)
            else:
                print("Senior does not have a phone number. Skipping SMS.")

            if senior_user.email:
                print("Senior has an email. Attempting to send email.")
                send_email(
                    app, senior_user.email, "Missed Appointment Alert", senior_msg
                )
            else:
                print("Senior does not have an email. Skipping email.")

            # --- 2. Notify the Caregiver ---
            assignment = CaregiverAssignment.query.filter_by(
                senior_id=senior_user.user_id
            ).first()
            if assignment and (
                caregiver_user := User.query.get(assignment.caregiver_id)
            ):
                print(
                    f"Found caregiver: {caregiver_user.username}. Email: '{caregiver_user.email}', Phone: '{caregiver_user.phone_number}'"
                )
                caregiver_msg = (
                    f"ALERT: {senior_user.name}'s appointment for '{appt.title}' "
                    f"on {formatted_time} was missed. Please follow up with them."
                )

                if caregiver_user.phone_number:
                    print("Caregiver has a phone number. Attempting to send SMS.")
                    send_sms(caregiver_user.phone_number, caregiver_msg)
                else:
                    print("Caregiver does not have a phone number. Skipping SMS.")

                if caregiver_user.email:
                    print("Caregiver has an email. Attempting to send email.")
                    send_email(
                        app,
                        caregiver_user.email,
                        f"Missed Appointment for {senior_user.username}",
                        caregiver_msg,
                    )
                else:
                    print("Caregiver does not have an email. Skipping email.")
            else:
                print("No assigned caregiver found for this senior.")

            db.session.add(senior_user.senior_citizen)
            db.session.add(appt)

        db.session.commit()
        print("--- Finished processing and committed to DB. ---")


@celery_app.task
# --- 1. UPDATE THE FUNCTION SIGNATURE ---
def send_emergency_alert(senior_id, latitude=None, longitude=None):
    app = get_flask_app()
    with app.app_context():
        from models import User, CaregiverAssignment

        senior_user = User.query.get(senior_id)
        if not senior_user:
            return

        # --- 2. CREATE A GOOGLE MAPS LINK ---
        if latitude and longitude:
            # This is the correct, standard URL for Google Maps
            maps_link = f"https://maps.google.com/?q={latitude},{longitude}"
            alert_msg = (
                f"EMERGENCY ALERT: {senior_user.username} has triggered an emergency alert. "
                f"Their current location is: {maps_link}"
            )
        else:
            alert_msg = (
                f"EMERGENCY ALERT: {senior_user.name} has triggered an emergency alert. "
                "Their location could not be determined. Please check on them immediately."
            )

        # Notify the assigned caregiver
        assignment = CaregiverAssignment.query.filter_by(
            senior_id=senior_user.user_id
        ).first()
        if assignment and (caregiver_user := User.query.get(assignment.caregiver_id)):
            print(f"Notifying assigned caregiver: {caregiver_user.name}")
            if caregiver_user.phone_number:
                send_sms(caregiver_user.phone_number, alert_msg)
            # --- FIX: Check if email exists before sending ---
            if caregiver_user.email:
                send_email(app, caregiver_user.email, "EMERGENCY ALERT!", alert_msg)

        # Notify all emergency contacts
        for contact in getattr(senior_user, "emergency_contacts", []):
            print(f"Notifying emergency contact: {contact.name}")
            if contact.phone:
                send_sms(contact.phone, alert_msg)
            # --- FIX: Check if email exists before sending ---
            if hasattr(contact, "email") and contact.email:
                send_email(app, contact.email, "EMERGENCY ALERT!", alert_msg)


@celery_app.task
def notify_caregiver_medication_taken(medication_id):
    """Notifies the caregiver that a medication has been marked as taken."""
    app = get_flask_app()
    with app.app_context():
        from models import Medication, User, CaregiverAssignment

        med = Medication.query.get(medication_id)
        if not med:
            print(f"Medication taken notification: Med ID {medication_id} not found.")
            return

        senior_user = User.query.get(med.senior_id)
        if not senior_user:
            return

        # Find the assigned caregiver
        assignment = CaregiverAssignment.query.filter_by(
            senior_id=senior_user.user_id
        ).first()
        if assignment and (caregiver := User.query.get(assignment.caregiver_id)):

            # Format time to IST for the message
            ist_tz = pytz.timezone("Asia/Kolkata")
            taken_time_ist = datetime.now(ist_tz).strftime("%I:%M %p")

            msg = (
                f"✅ Confirmation: {senior_user.name} marked their medication "
                f"'{med.name}' ({med.dosage}) as taken at {taken_time_ist}."
            )

            if caregiver.phone_number:
                send_sms(caregiver.phone_number, msg)
            if caregiver.email:
                send_email(app, caregiver.email, f"Medication Taken: {med.name}", msg)

            print(
                f"Sent 'medication taken' notification to caregiver {caregiver.name}."
            )
