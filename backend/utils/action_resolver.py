from datetime import datetime, timedelta, timezone
from models import (
    Appointment,
    Medication,
    EmergencyContact,
    Feedback,
    Event,
    SeniorCitizen,
)


def resolve_action(intent: str, senior_id: str, entities: dict = {}) -> str:
    """Resolves an AI-recognized intent into a specific database query and response."""

    response_text = ""
    senior = SeniorCitizen.query.get(senior_id)

    if not senior:
        return "I cannot find information for that senior."

    if intent == "get_next_appointment":
        now = datetime.now(timezone.utc)
        next_appointment = (
            Appointment.query.filter(
                Appointment.senior_id == senior_id, Appointment.date_time > now
            )
            .order_by(Appointment.date_time.asc())
            .first()
        )

        if next_appointment:
            date_str = next_appointment.date_time.strftime("%A, %B %d at %I:%M %p")
            response_text = (
                f"Your next appointment is on {date_str} with {next_appointment.title}."
            )
        else:
            response_text = "You have no upcoming appointments."

    elif intent == "get_medication_schedule":
        now = datetime.now(timezone.utc)
        next_medication = (
            Medication.query.filter(
                Medication.senior_id == senior_id, Medication.time > now
            )
            .order_by(Medication.time.asc())
            .first()
        )

        if next_medication:
            time_str = next_medication.time.strftime("%I:%M %p")
            response_text = f"You need to take {next_medication.name} at {time_str}."
        else:
            response_text = "You have no upcoming medications scheduled."

    elif intent == "get_emergency_contacts":
        contacts = EmergencyContact.query.filter_by(senior_id=senior_id).all()
        if contacts:
            contact_list = ", ".join([c.name for c in contacts])
            response_text = f"Your emergency contacts are: {contact_list}."
        else:
            response_text = "You have not added any emergency contacts yet."

    elif intent == "get_medication_history_caregiver":
        one_week_ago = datetime.now(timezone.utc) - timedelta(weeks=1)
        medications_taken = Medication.query.filter(
            Medication.senior_id == senior_id,
            Medication.isTaken,
            Medication.time >= one_week_ago,
        ).all()

        if medications_taken:
            med_list = ", ".join(
                [
                    f"{m.name} at {m.time.strftime('%I:%M %p on %b %d')}"
                    for m in medications_taken
                ]
            )
            response_text = f"Your father has taken the following medications this week: {med_list}."
        else:
            response_text = (
                "Your father has not taken any recorded medications this week."
            )

    elif intent == "get_pending_appointments_caregiver":
        start_of_month = datetime.now(timezone.utc).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        pending_appointments = Appointment.query.filter(
            Appointment.senior_id == senior_id,
            Appointment.status != "Completed",
            Appointment.date_time >= start_of_month,
        ).all()

        if pending_appointments:
            app_list = ", ".join(
                [
                    f"{a.title} on {a.date_time.strftime('%b %d at %I:%M %p')}"
                    for a in pending_appointments
                ]
            )
            response_text = f"Your father has the following pending appointments this month: {app_list}."
        else:
            response_text = "Your father has no pending appointments this month."

    elif intent == "get_news_summary":
        recent_news = Feedback.query.order_by(Feedback.created_at.desc()).limit(3).all()
        if recent_news:
            news_list = "\n".join([f"- {n.title} from {n.source}" for n in recent_news])
            response_text = f"Here are some recent news headlines:\n{news_list}"
        else:
            response_text = "I could not find any recent news."

    elif intent == "get_event_details":
        now = datetime.now(timezone.utc)
        upcoming_events = (
            Event.query.filter(Event.date_time > now)
            .order_by(Event.date_time.asc())
            .limit(3)
            .all()
        )
        if upcoming_events:
            event_list = "\n".join(
                [
                    f"- {e.name} on {e.date_time.strftime('%b %d at %I:%M %p')} at {e.location}"
                    for e in upcoming_events
                ]
            )
            response_text = f"Here are some upcoming events:\n{event_list}"
        else:
            response_text = "I could not find any upcoming events."

    elif intent == "get_user_stats":
        response_text = (
            f"Here are {senior.user.username}'s stats:\n"
            f"- Age: {senior.age}\n"
            f"- Topics Liked: {senior.topics_liked}\n"
            f"- Comments Posted: {senior.comments_posted}\n"
            f"- Appointments Missed: {senior.appointments_missed}\n"
            f"- Medications Missed: {senior.medications_missed}\n"
            f"- Total Screentime: {senior.total_screentime} minutes"
        )

    else:  # unknown intent
        response_text = "I'm sorry, I don't understand that request. Please try asking about appointments, medications, news, events, or user statistics."

    return response_text
