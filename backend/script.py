# script.py
from datetime import datetime, timedelta, timezone
import secrets

from flask import Flask
from extensions import db
from models import (
    Role,
    User,
    SeniorCitizen,
    Caregiver,
    CaregiverAssignment,
    ServiceProvider,
    Event,
    Appointment,
    Medication,
    EmergencyContact,
)

# Flask app + DB setup
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///senior_citizen.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def create_dummy_data():
    db.drop_all()
    db.create_all()

    # Roles
    role_senior = Role(name="senior", description="Senior Citizen")
    role_caregiver = Role(name="caregiver", description="Caregiver")
    db.session.add_all([role_senior, role_caregiver])

    # Senior User
    senior_user = User(
        username="senior1",
        email="senior1@example.com",
        password="password123",
        name="John Senior",
        fs_uniquifier=secrets.token_urlsafe(32),
        created_at=datetime.now(timezone.utc),
    )
    senior_user.roles.append(role_senior)
    senior = SeniorCitizen(
        user=senior_user,
        age=75,
        font_size="medium",
        theme="light",
        news_categories="health,technology",
    )

    # Caregiver User
    caregiver_user = User(
        username="caregiver1",
        email="caregiver1@example.com",
        password="password123",
        name="Jane Caregiver",
        fs_uniquifier=secrets.token_urlsafe(32),
        created_at=datetime.now(timezone.utc),
    )
    caregiver_user.roles.append(role_caregiver)
    caregiver = Caregiver(user=caregiver_user)

    # Assignment
    assignment = CaregiverAssignment(caregiver=caregiver, senior=senior)

    # Service Provider
    sp = ServiceProvider(
        name="Happy Seniors Services",
        contact_email="contact@hss.com",
        phone_number="1234567890",
        services_offered="events,healthcare",
    )

    # Event
    event = Event(
        name="Health Checkup Camp",
        date_time=datetime.now(timezone.utc) + timedelta(days=3),
        location="Community Center",
        description="Free health checkups for seniors.",
        service_provider=sp,
    )

    # Appointment for Senior
    appointment = Appointment(
        title="Doctor Visit",
        date_time=datetime.now(timezone.utc) + timedelta(days=2),
        location="City Hospital",
        senior=senior,
    )

    # Medication for Senior
    medication = Medication(
        name="Aspirin",
        dosage="75mg",
        time=datetime.now(timezone.utc) + timedelta(hours=5),
        senior=senior,
    )

    # Emergency Contact
    emergency_contact = EmergencyContact(
        name="Mike Emergency",
        relation="Son",
        phone="9876543210",
        email="mike@example.com",
        senior=senior_user,
    )

    db.session.add_all(
        [
            senior_user,
            senior,
            caregiver_user,
            caregiver,
            assignment,
            sp,
            event,
            appointment,
            medication,
            emergency_contact,
        ]
    )
    db.session.commit()
    print("Dummy data created successfully!")


if __name__ == "__main__":
    with app.app_context():
        create_dummy_data()
