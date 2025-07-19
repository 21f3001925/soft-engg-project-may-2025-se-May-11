from celery_app import celery_app
from extensions import socketio
from utils.notification import send_sms, send_email
from models import User, Medication
from datetime import datetime, timedelta
from flask import current_app
import requests


@celery_app.task
def send_reminder_notification(appointment_id, title, location, date_time, user_email):
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
    medication = Medication.query.get(medication_id)
    if medication and not medication.isTaken:
        user = User.query.get(medication.senior_id)
        if user:
            send_sms(
                user.phone_number,
                f"Reminder: Take {medication.dosage} of {medication.name}",
            )


@celery_app.task
def send_event_reminder(user_id, event_name, event_location, event_time):
    user = User.query.get(user_id)
    if user:
        send_sms(
            user.phone_number,
            f"Reminder: {event_name} at {event_location} on {event_time}",
        )


@celery_app.task
def send_daily_news_update(user_id):
    user = User.query.get(user_id)
    if user:
        news_api_key = current_app.config.get("NEWSAPI_KEY")
        if not news_api_key:
            return

        try:
            category = user.senior_citizen.news_categories or "general"
            response = requests.get(
                f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={news_api_key}"
            )
            response.raise_for_status()
            articles = response.json().get("articles", [])[:5]
            news_summary = "Your Daily News Update:\n\n" + "".join(
                f"- {article['title']} ({article['source']['name']})\n  Read more: {article['url']}\n\n"
                for article in articles
            )
            send_email(current_app, user.email, "Your Daily News Update", news_summary)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news for {user.username}: {e}")


@celery_app.task
def check_missed_medications():
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)

    missed_meds = Medication.query.filter(
        Medication.isTaken.is_(False), Medication.time <= one_hour_ago
    ).all()

    for med in missed_meds:
        senior = User.query.get(med.senior_id)
        if senior and senior.caregiver_id:
            caregiver = User.query.get(senior.caregiver_id)
            if caregiver:
                message = f"ALERT: {senior.username} missed {med.dosage} of {med.name} due at {med.time.strftime('%H:%M')}"
                send_sms(caregiver.phone_number, message)
                send_email(
                    current_app, caregiver.email, "Missed Medication Alert", message
                )


@celery_app.task
def send_emergency_alert(senior_id):
    senior = User.query.get(senior_id)
    if senior:
        caregiver = User.query.get(senior.caregiver_id)
        alert_message = (
            f"EMERGENCY ALERT: {senior.username} has pressed the emergency button!"
        )

        if caregiver:
            send_sms(caregiver.phone_number, alert_message)
            send_email(current_app, caregiver.email, "EMERGENCY ALERT!", alert_message)

        for contact in senior.emergency_contacts:
            send_sms(contact.phone, alert_message)
            send_email(contact.email, "EMERGENCY ALERT!", alert_message)
