# tasks.py
from celery_app import celery_app
from extensions import socketio
from celery_app import Celery as celery
from utils.notification import send_sms, send_email
from models import User, Medication
from datetime import datetime, timedelta
from flask import current_app
import requests


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


@celery.task
def send_medication_reminder(medication_id):
    with current_app.app_context():
        medication = Medication.query.get(medication_id)
        if medication and not medication.isTaken:
            user = User.query.get(medication.senior_id)
            if user:
                print(
                    f"Medication Reminder for {user.username}: Take {medication.dosage} of {medication.name}"
                )
                send_sms(
                    user.phone_number,
                    f"Reminder: Take {medication.dosage} of {medication.name}",
                )


@celery.task
def send_event_reminder(user_id, event_name, event_location, event_time):
    with current_app.app_context():
        user = User.query.get(user_id)
        if user:
            print(
                f"Event Reminder for {user.username}: {event_name} at {event_location} on {event_time}"
            )
            send_sms(
                user.phone_number,
                f"Reminder: {event_name} at {event_location} on {event_time}",
            )


@celery.task
def send_daily_news_update(user_id):
    with current_app.app_context():
        user = User.query.get(user_id)
        if user:
            news_api_key = current_app.config.get("NEWSAPI_KEY")
            if not news_api_key:
                print("NEWSAPI_KEY not configured. Skipping daily news update.")
                return

            try:
                # Fetch news based on user preferences
                category = (
                    user.senior_citizen.news_categories
                    if user.senior_citizen and user.senior_citizen.news_categories
                    else "general"
                )
                response = requests.get(
                    f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={news_api_key}"
                )
                response.raise_for_status()
                articles = response.json().get("articles", [])[:5]  # Get top 5 articles
                news_summary = "Your Daily News Update:\n\n"
                for article in articles:
                    news_summary += (
                        f"- {article['title']} ({article['source']['name']})\n"
                    )
                    news_summary += f"  Read more: {article['url']}\n\n"
                print(f"Daily News for {user.username}:\n{news_summary}")
                send_email(
                    current_app, user.email, "Your Daily News Update", news_summary
                )
            except requests.exceptions.RequestException as e:
                print(f"Error fetching news for {user.username}: {e}")


@celery.task
def check_missed_medications():
    with current_app.app_context():
        # This task would typically run periodically (e.g., every 15-30 minutes)
        # and check for medications that should have been taken but aren't marked as such.
        # For demonstration, let's assume we check for medications due in the last hour
        # that are not marked as taken.
        now = datetime.utcnow()
        one_hour_ago = now - timedelta(hours=1)

        missed_meds = Medication.query.filter(
            not Medication.isTaken, Medication.time <= one_hour_ago
        ).all()

        for med in missed_meds:
            senior = User.query.get(med.senior_id)
            if senior and senior.caregiver_id:
                caregiver = User.query.get(senior.caregiver_id)
                if caregiver:
                    message = f"ALERT: {senior.username} missed their {med.dosage} of {med.name} due at {med.time.strftime('%H:%M')}."
                    print(
                        f"Missed Medication Alert for {caregiver.username}: {message}"
                    )
                    send_sms(caregiver.phone_number, message)
                    send_email(
                        current_app, caregiver.email, "Missed Medication Alert", message
                    )


@celery.task
def send_emergency_alert(senior_id):
    with current_app.app_context():
        senior = User.query.get(senior_id)
        if senior:
            emergency_contacts = senior.emergency_contacts
            caregiver = User.query.get(senior.caregiver_id)

            alert_message = f"EMERGENCY ALERT: {senior.username} has pressed the emergency button! Please check on them immediately."

            # Notify caregiver
            if caregiver:
                print(
                    f"Emergency Alert to Caregiver {caregiver.username}: {alert_message}"
                )
                send_sms(caregiver.phone_number, alert_message)
                send_email(
                    current_app, caregiver.email, "EMERGENCY ALERT!", alert_message
                )

            # Notify emergency contacts
            for contact in emergency_contacts:
                print(
                    f"Emergency Alert to Contact {contact.name}: {alert_message} (Phone: {contact.phone})"
                )
                send_sms(contact.phone, alert_message)
                send_email(contact.email, "EMERGENCY ALERT!", alert_message)
