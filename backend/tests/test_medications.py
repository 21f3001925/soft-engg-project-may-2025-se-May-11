from datetime import datetime, timezone, timedelta
import uuid
import json

from models import Medication, User, db


class TestDatabaseConfiguration:

    def test_uses_in_memory_database(self, app):
        with app.app_context():
            assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
            assert app.config["TESTING"] is True


class TestMedicationModel:

    def test_creates_medication_with_all_fields(self, senior_user):
        expected_medication_name = "Aspirin"
        expected_dosage = "10mg"
        expected_time = datetime.now(timezone.utc) + timedelta(hours=1)

        medication = Medication(
            name=expected_medication_name,
            dosage=expected_dosage,
            time=expected_time,
            isTaken=False,
            senior_id=senior_user.user_id,
        )
        db.session.add(medication)
        db.session.commit()

        saved_medication = Medication.query.filter_by(
            name=expected_medication_name
        ).first()
        assert saved_medication is not None
        assert saved_medication.name == expected_medication_name
        assert saved_medication.dosage == expected_dosage
        assert saved_medication.isTaken is False
        assert saved_medication.senior_id == senior_user.user_id

    def test_get_all_medication_api(self, client, auth_headers):
        response = client.get(
            "/api/v1/medications",
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 200

    def test_create_medication_api(self, client, auth_headers):
        response = client.post(
            "/api/v1/medications",
            headers=auth_headers,
            json={
                "name": "Aspirin",
                "dosage": "10mg",
                "time": datetime.now(timezone.utc).isoformat(),
            },
        )
        data = response.get_json()
        assert response.status_code == 201
        assert data["message"] == "Medication added"

    def test_create_medication_with_extra_field_api(self, client, auth_headers):
        response = client.post(
            "/api/v1/medications",
            headers=auth_headers,
            json={
                "name": "Aspirin",
                "dosage": "10mg",
                "time": datetime.now(timezone.utc).isoformat(),
                "extra_field": "Wrong field for test",
            },
        )
        data = response.get_json()
        assert response.status_code == 422

    def test_get_medication_with_medication_id_api(self, client, auth_headers, sample_medication):
        medication_id = sample_medication.medication_id
        response = client.get(
            f"/api/v1/medications/{medication_id}",
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 200

    def test_update_medication_with_medication_id_api(self, client, auth_headers, sample_medication):
        medication_id = sample_medication.medication_id
        response = client.put(
            f"/api/v1/medications/{medication_id}",
            headers=auth_headers,
            json={
                "name": "Updated Aspirin",
                "dosage": "2090mg",
                "time": datetime.now(timezone.utc).isoformat(),
                "isTaken": True,
            },
        )
        data = response.get_json()
        assert response.status_code == 200

    #Error code 422 for PUT test case
    def test_update_medication_with_medication_id_using_wrong_fields_api(self, client, auth_headers, sample_medication):
        medication_id = sample_medication.medication_id
        response = client.put(
            f"/api/v1/medications/{medication_id}",
            headers=auth_headers,
            json={
                "name": "Updated Aspirin",
                "dosage": "2090mg",
                "time": datetime.now(timezone.utc).isoformat(),
                "isTaken": True,
                "extra_field": "Wrong field for test",
            },
        )
        data = response.get_json()
        assert response.status_code == 422

    def test_delete_medication_with_medication_id_api(self, client, auth_headers, sample_medication):
        medication_id = sample_medication.medication_id
        response = client.delete(
            f"/api/v1/medications/{medication_id}",
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data["message"] == "Medication deleted"

    def test_applies_default_values_when_not_specified(self, senior_user):
        vitamin_d_medication = Medication(
            name="Vitamin D",
            dosage="1000 IU",
            time=datetime.now(timezone.utc),
            senior_id=senior_user.user_id,
        )
        db.session.add(vitamin_d_medication)
        db.session.commit()

        assert vitamin_d_medication.isTaken is False
        assert vitamin_d_medication.medication_id is not None

    def test_generates_unique_ids_for_different_medications(self, senior_user):
        morning_pill = Medication(
            name="Morning Pill",
            dosage="5mg",
            time=datetime.now(timezone.utc),
            senior_id=senior_user.user_id,
        )
        evening_pill = Medication(
            name="Evening Pill",
            dosage="10mg",
            time=datetime.now(timezone.utc),
            senior_id=senior_user.user_id,
        )
        db.session.add_all([morning_pill, evening_pill])
        db.session.commit()

        assert morning_pill.medication_id != evening_pill.medication_id
        assert uuid.UUID(morning_pill.medication_id)
        assert uuid.UUID(evening_pill.medication_id)

    def test_toggles_taken_status_correctly(self, sample_medication):
        medication = sample_medication
        assert medication.isTaken is False

        medication.isTaken = True
        db.session.commit()
        updated_medication = Medication.query.filter_by(
            medication_id=medication.medication_id
        ).first()
        assert updated_medication.isTaken is True

        medication.isTaken = False
        db.session.commit()
        updated_medication = Medication.query.filter_by(
            medication_id=medication.medication_id
        ).first()
        assert updated_medication.isTaken is False


class TestMedicationUserRelationship:

    def test_medication_belongs_to_correct_user(self, sample_medication, senior_user):
        assert sample_medication.senior_id == senior_user.user_id

    def test_user_can_have_multiple_medications(self, senior_user):
        blood_pressure_medication = Medication(
            name="Blood Pressure Medication",
            dosage="5mg",
            senior_id=senior_user.user_id,
            time=datetime.now(timezone.utc),
        )
        diabetes_medication = Medication(
            name="Diabetes Medication",
            dosage="10mg",
            senior_id=senior_user.user_id,
            time=datetime.now(timezone.utc),
        )
        db.session.add_all([blood_pressure_medication, diabetes_medication])
        db.session.commit()

        user_medications = Medication.query.filter_by(
            senior_id=senior_user.user_id
        ).all()
        assert len(user_medications) == 2
        medication_names = {med.name for med in user_medications}
        assert medication_names == {"Blood Pressure Medication", "Diabetes Medication"}

    def test_finds_user_medications_in_database(self, sample_medication, senior_user):
        user_medications = Medication.query.filter_by(
            senior_id=senior_user.user_id
        ).all()

        assert len(user_medications) == 1
        assert user_medications[0].medication_id == sample_medication.medication_id


class TestUserRoleAssignment:

    def test_senior_user_has_correct_role(self, senior_user):
        found_user = User.query.filter_by(username=senior_user.username).first()

        assert found_user is not None
        assert len(found_user.roles) == 1
        assert found_user.roles[0].name == "senior_citizen"

    def test_caregiver_user_has_correct_role(self, caregiver_user):
        found_user = User.query.filter_by(username=caregiver_user.username).first()

        assert found_user is not None
        assert len(found_user.roles) == 1
        assert found_user.roles[0].name == "caregiver"


class TestMedicationAPIAuthentication:

    def test_get_medications_requires_authentication(self, client):
        response = client.get("/api/v1/medications")
        assert response.status_code == 401

    def test_post_medications_requires_authentication(self, client):
        response = client.post("/api/v1/medications")
        assert response.status_code == 401

    def test_get_specific_medication_requires_authentication(self, client):
        medication_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/medications/{medication_id}")
        assert response.status_code == 401

    def test_update_medication_requires_authentication(self, client):
        medication_id = str(uuid.uuid4())
        response = client.put(f"/api/v1/medications/{medication_id}")
        assert response.status_code == 401

    def test_delete_medication_requires_authentication(self, client):
        medication_id = str(uuid.uuid4())
        response = client.delete(f"/api/v1/medications/{medication_id}")
        assert response.status_code == 401


class TestMedicationAPIAuthorization:

    def test_get_medications_with_empty_list(self, client, auth_headers):
        response = client.get("/api/v1/medications", headers=auth_headers)
        assert response.status_code == 200

    def test_get_medication_requires_authorization(self, client, auth_headers):
        medication_id = str(uuid.uuid4())
        response = client.get(
            f"/api/v1/medications/{medication_id}", headers=auth_headers
        )
        assert response.status_code == 404

    def test_update_medication_requires_authorization(self, client, auth_headers):
        medication_id = str(uuid.uuid4())
        medication_update_payload = {"name": "Updated Medication"}

        response = client.put(
            f"/api/v1/medications/{medication_id}",
            data=json.dumps(medication_update_payload),
            content_type="application/json",
            headers=auth_headers,
        )
        assert response.status_code == 400

    def test_delete_medication_requires_authorization(self, client, auth_headers):
        medication_id = str(uuid.uuid4())
        response = client.delete(
            f"/api/v1/medications/{medication_id}", headers=auth_headers
        )
        assert response.status_code == 400


class TestMedicationAPIValidation:

    def test_create_medication_with_empty_payload_fails(self, client, auth_headers):
        empty_medication_payload = {}

        response = client.post(
            "/api/v1/medications",
            data=json.dumps(empty_medication_payload),
            content_type="application/json",
            headers=auth_headers,
        )

        assert response.status_code == 422

    def test_create_medication_without_name_fails(self, client, auth_headers):
        medication_payload_without_name = {
            "dosage": "10mg",
            "time": datetime.now(timezone.utc).isoformat(),
            "isTaken": False,
        }

        response = client.post(
            "/api/v1/medications",
            data=json.dumps(medication_payload_without_name),
            content_type="application/json",
            headers=auth_headers,
        )

        assert response.status_code == 422

    def test_create_medication_without_dosage_fails(self, client, auth_headers):
        medication_payload_without_dosage = {
            "name": "Aspirin",
            "time": datetime.now(timezone.utc).isoformat(),
            "isTaken": False,
        }

        response = client.post(
            "/api/v1/medications",
            data=json.dumps(medication_payload_without_dosage),
            content_type="application/json",
            headers=auth_headers,
        )

        assert response.status_code == 422

    def test_create_medication_with_invalid_time_format_fails(
        self, client, auth_headers
    ):
        medication_payload_with_invalid_time = {
            "name": "Aspirin",
            "dosage": "10mg",
            "time": "not-a-valid-datetime",
            "isTaken": False,
        }

        response = client.post(
            "/api/v1/medications",
            data=json.dumps(medication_payload_with_invalid_time),
            content_type="application/json",
            headers=auth_headers,
        )

        assert response.status_code == 400
