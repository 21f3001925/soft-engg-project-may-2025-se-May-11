from app import app
from models import db, User, SeniorCitizen, Medication
from tasks import send_medication_reminder
from datetime import datetime, timezone


with app.app_context():
    # Create dummy user if not exists
    senior_user = User.query.filter_by(username="test_senior_user").first()
    if not senior_user:
        print("Creating dummy senior user...")
        senior_user = User(
            username="test_senior_user",
            email="test_senior@example.com",
            password="your_password_here",
            name="Test Senior",
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
    send_medication_reminder.delay(test_medication_id)
    print("Task sent to Celery.")
