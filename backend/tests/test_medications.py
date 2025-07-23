from datetime import datetime, timezone, timedelta
import bcrypt

from models import Medication, User, Role, db


class TestMedicationsAPI:

    def test_using_test_database(self, app):
        with app.app_context():
            db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
            assert db_uri == "sqlite:///:memory:"
            assert app.config["TESTING"] is True

    def create_test_user(self, username="test_senior", role_name="senior_citizen"):
        role = Role(name=role_name, description=f"{role_name} role")
        db.session.add(role)
        db.session.flush()

        hashed_pw = bcrypt.hashpw(
            "TestPassword123!".encode(), bcrypt.gensalt()
        ).decode()
        user = User(
            username=username,
            email=f"{username}@test.com",
            password=hashed_pw,
            phone_number="+1234567890",
            name=f"Test {username}",
        )
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        return user

    def test_medication_model_creation(self):
        user = self.create_test_user("test_senior", "senior_citizen")

        medication = Medication(
            name="Test Medication",
            dosage="10mg",
            time=datetime.now(timezone.utc) + timedelta(hours=1),
            isTaken=False,
            senior_id=user.user_id,
        )
        db.session.add(medication)
        db.session.commit()

        saved_med = Medication.query.filter_by(name="Test Medication").first()
        assert saved_med is not None
        assert saved_med.name == "Test Medication"
        assert saved_med.dosage == "10mg"
        assert saved_med.isTaken is False
        assert saved_med.senior_id == user.user_id

    def test_user_role_assignment(self):
        user = self.create_test_user("test_senior", "senior_citizen")

        found_user = User.query.filter_by(username=user.username).first()
        assert found_user is not None
        assert found_user.roles[0].name == "senior_citizen"

    def test_multiple_medications_for_user(self):
        user = self.create_test_user("test_senior", "senior_citizen")

        med1 = Medication(
            name="Med 1",
            dosage="5mg",
            senior_id=user.user_id,
            time=datetime.now(timezone.utc),
        )
        med2 = Medication(
            name="Med 2",
            dosage="10mg",
            senior_id=user.user_id,
            time=datetime.now(timezone.utc),
        )

        db.session.add_all([med1, med2])
        db.session.commit()

        user_meds = Medication.query.filter_by(senior_id=user.user_id).all()
        assert len(user_meds) == 2
        assert {med.name for med in user_meds} == {"Med 1", "Med 2"}

    def test_get_medications_unauthorized(self, client):
        response = client.get("/api/v1/medications")
        assert response.status_code == 401
