import uuid
from datetime import datetime, timedelta, timezone

from werkzeug.security import generate_password_hash
from extensions import db
from app import create_app  # assuming you have create_app in your Flask app
from models import (
    Role,
    User,
    SeniorCitizen,
    Caregiver,
    CaregiverAssignment,
    Appointment,
    Medication,
    EmergencyContact,
    Feedback,
    ServiceProvider,
    Event,
    EventAttendance,
    Alert,
    AlertType,
    ReferenceType,
)

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create Roles
    role_senior = Role(name="senior", description="Senior citizen user")
    role_caregiver = Role(name="caregiver", description="Caregiver user")
    db.session.add_all([role_senior, role_caregiver])
    db.session.commit()

    # Create Users
    senior_user = User(
        username="john_senior",
        email="john@example.com",
        password=generate_password_hash("password123"),
        age=75,
        city="New York",
        country="USA",
        phone_number="1234567890",
        name="John Doe",
    )
    senior_user.roles.append(role_senior)

    caregiver_user = User(
        username="mary_caregiver",
        email="mary@example.com",
        password=generate_password_hash("password123"),
        age=45,
        city="New York",
        country="USA",
        phone_number="0987654321",
        name="Mary Smith",
    )
    caregiver_user.roles.append(role_caregiver)

    db.session.add_all([senior_user, caregiver_user])
    db.session.commit()

    # SeniorCitizen & Caregiver profiles
    senior_profile = SeniorCitizen(
        user_id=senior_user.user_id,
        font_size="medium",
        theme="light",
        news_categories="health,finance",
        topics_liked=5,
        comments_posted=2,
    )
    caregiver_profile = Caregiver(user_id=caregiver_user.user_id)
    db.session.add_all([senior_profile, caregiver_profile])
    db.session.commit()

    # Assign caregiver to senior
    assignment = CaregiverAssignment(
        caregiver_id=caregiver_profile.user_id, senior_id=senior_profile.user_id
    )
    db.session.add(assignment)

    # Emergency Contact
    contact = EmergencyContact(
        name="Jane Emergency",
        relation="Daughter",
        phone="555-1234",
        email="jane@example.com",
        senior_id=senior_user.user_id,
    )
    db.session.add(contact)

    # Appointment
    appointment = Appointment(
        title="Doctor Visit",
        date_time=datetime.now(timezone.utc) + timedelta(days=2),
        location="City Clinic",
        reminder_time=datetime.now(timezone.utc) + timedelta(days=1),
        senior_id=senior_profile.user_id,
    )
    db.session.add(appointment)

    # Medication
    medication = Medication(
        name="Aspirin",
        dosage="1 pill",
        time=datetime.now(timezone.utc) + timedelta(hours=8),
        senior_id=senior_profile.user_id,
    )
    db.session.add(medication)

    # Service Provider & Event
    provider = ServiceProvider(
        name="Community Center",
        contact_email="info@community.org",
        phone_number="555-9876",
        services_offered="Health workshops, exercise classes",
    )
    db.session.add(provider)
    db.session.commit()

    event = Event(
        name="Yoga for Seniors",
        date_time=datetime.now(timezone.utc) + timedelta(days=3),
        location="Community Hall",
        description="Gentle yoga session",
        service_provider_id=provider.service_provider_id,
    )
    db.session.add(event)
    db.session.commit()

    # Event Attendance
    attendance = EventAttendance(
        senior_id=senior_profile.user_id, event_id=event.event_id
    )
    db.session.add(attendance)

    # Alert
    alert = Alert(
        recipient_user_id=senior_user.user_id,
        alert_type=AlertType.missed_medication,
        message="You missed your morning Aspirin dose.",
        reference_type=ReferenceType.medication,
        reference_id=medication.medication_id,
    )
    db.session.add(alert)

    # Feedback/News
    news = Feedback(
        api_article_id=str(uuid.uuid4()),
        title="Senior Health Tips",
        description="Daily exercises for seniors to stay healthy",
        url="https://example.com/article",
        source="Health News",
        category="health",
    )
    db.session.add(news)

    db.session.commit()
    print("✅ Database populated with sample data.")
