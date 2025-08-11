from app_factory import create_app
from models import db, User, SeniorCitizen, EmergencyContact, Role
from tasks import send_emergency_alert

TEST_SENIOR_USERNAME = "test_senior_for_emergency"
TEST_SENIOR_EMAIL = "your-real-email"

# Use real contact details here to receive the test alerts
TEST_CONTACT_1_PHONE = "+91123132132"
TEST_CONTACT_1_EMAIL = "email@gmail.com"

TEST_CONTACT_2_PHONE = "+91123123123"
TEST_CONTACT_2_EMAIL = "email@gmail.com"


def create_test_data(app):
    """Creates a dummy senior, role, and emergency contacts for testing."""
    with app.app_context():

        senior_role = Role.query.filter_by(name="senior_citizen").first()
        if not senior_role:
            print("Creating 'senior_citizen' role...")
            senior_role = Role(
                name="senior_citizen", description="A senior citizen user"
            )
            db.session.add(senior_role)
            db.session.commit()

        senior_user = User.query.filter_by(username=TEST_SENIOR_USERNAME).first()
        if not senior_user:
            print(f"Creating dummy senior user: {TEST_SENIOR_USERNAME}")
            senior_user = User(
                username=TEST_SENIOR_USERNAME,
                email=TEST_SENIOR_EMAIL,
                password="password",
                name="Test Emergency Senior",
                roles=[senior_role],
            )
            db.session.add(senior_user)
            db.session.commit()

            senior_profile = SeniorCitizen(user_id=senior_user.user_id)
            db.session.add(senior_profile)
            db.session.commit()
        else:
            print(f"Found existing senior user: {TEST_SENIOR_USERNAME}")

        if not senior_user.emergency_contacts:
            print("Creating dummy emergency contacts...")
            contact1 = EmergencyContact(
                name="John Doe",
                phone=TEST_CONTACT_1_PHONE,
                email=TEST_CONTACT_1_EMAIL,
                senior_id=senior_user.user_id,
            )
            contact2 = EmergencyContact(
                name="Jane Smith",
                phone=TEST_CONTACT_2_PHONE,
                email=TEST_CONTACT_2_EMAIL,
                senior_id=senior_user.user_id,
            )
            db.session.add_all([contact1, contact2])
            db.session.commit()
            print("Emergency contacts created.")
        else:
            print("Emergency contacts already exist for this user.")

        return senior_user.user_id


def run_test():
    """Triggers the emergency alert task for the test user."""
    flask_app = create_app()
    senior_id_to_test = create_test_data(flask_app)

    print("\n" + "=" * 50)
    print(f"--- Triggering Emergency Alert for user_id: {senior_id_to_test} ---")
    print("=" * 50 + "\n")

    result = send_emergency_alert.delay(senior_id_to_test)

    print(f"Task 'send_emergency_alert' sent to Celery with task ID: {result.id}")
    print("Check your Celery worker logs to see the SMS and Email sending status.")
    print("Check the recipient inboxes for the alert messages.")


if __name__ == "__main__":
    run_test()
