from app_factory import create_app
from models import db, User, SeniorCitizen, Medication
from tasks import send_medication_reminder
from datetime import datetime, timezone

app = create_app()

with app.app_context():
    # Create dummy user
    senior_user = User.query.filter_by(username="rishit").first()
    if not senior_user:
        print("Creating dummy senior user...")
        senior_user = User(
            username="rishit",
            email="put original your email",
            password="mypassword",
            name="rishit",
            phone_number="123",  # Add original phone number for testing.
        )
        db.session.add(senior_user)
        db.session.commit()

        senior_profile = SeniorCitizen(user_id=senior_user.user_id)
        db.session.add(senior_profile)
        db.session.commit()
        print(f"Dummy senior user created with ID: {senior_user.user_id}")
    else:
        print(f"Dummy senior user already exists with ID: {senior_user.user_id}")

    # Create dummy medication
    medication = Medication.query.filter_by(
        senior_id=senior_user.user_id, name="Test Medication"
    ).first()

    if not medication:
        print("Creating dummy medication...")
        medication = Medication(
            name="Test Medication",
            dosage="2 pills",
            time=datetime.now(timezone.utc),
            isTaken=False,
            senior_id=senior_user.user_id,
        )
        db.session.add(medication)
        db.session.commit()
        print(f"Dummy medication created with ID: {medication.medication_id}")
    else:
        print(f"Dummy medication already exists with ID: {medication.medication_id}")

    test_medication_id = medication.medication_id
    print(f"\nUse this medication ID for testing: {test_medication_id}")
    print(f"Triggering send_medication_reminder for ID: {test_medication_id}")

    result = send_medication_reminder.delay(test_medication_id)
    print(f"Task sent to Celery with ID: {result.id}")
