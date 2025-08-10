# script.py
from werkzeug.security import generate_password_hash
from extensions import db
from models import User, Role, SeniorCitizen, Caregiver, ServiceProvider
from app import app  # assuming app is defined in app.py

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create roles
    senior_role = Role(name="senior_citizen", description="Senior Citizen role")
    caregiver_role = Role(name="caregiver", description="Caregiver role")
    service_provider_role = Role(
        name="service_provider", description="Service Provider role"
    )
    db.session.add_all([senior_role, caregiver_role, service_provider_role])
    db.session.commit()

    # Create Senior Citizen user
    senior_user = User(
        username="senior1",
        email="senior1@example.com",
        password=generate_password_hash("password123"),
        name="John Senior",
    )
    senior_user.roles.append(senior_role)
    db.session.add(senior_user)
    db.session.commit()

    senior_profile = SeniorCitizen(
        user_id=senior_user.user_id, font_size="medium", theme="light"
    )
    db.session.add(senior_profile)

    # Create Caregiver user
    caregiver_user = User(
        username="caregiver1",
        email="caregiver1@example.com",
        password=generate_password_hash("password123"),
        name="Mary Care",
    )
    caregiver_user.roles.append(caregiver_role)
    db.session.add(caregiver_user)
    db.session.commit()

    caregiver_profile = Caregiver(user_id=caregiver_user.user_id)
    db.session.add(caregiver_profile)

    # Create Service Provider
    service_provider = ServiceProvider(
        name="Golden Care Services",
        contact_email="contact@goldencare.com",
        phone_number="123-456-7890",
        services_offered="Home Care, Nursing, Therapy",
    )
    db.session.add(service_provider)

    db.session.commit()

    print("Database populated successfully.")
