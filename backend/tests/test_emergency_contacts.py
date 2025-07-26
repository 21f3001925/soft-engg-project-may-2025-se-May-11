import uuid
import pytest
from flask_jwt_extended import create_access_token

from models import db, EmergencyContact, CaregiverAssignment
from extensions import db


class TestDatabaseConfiguration:

    def test_uses_in_memory_database(self, app):
        with app.app_context():
            assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
            assert app.config["TESTING"] is True


class TestEmergencyContactModel:

    def test_creates_emergency_contact_with_all_fields(self, senior_user):
        expected_name = "Emergency Contact"
        expected_relation = "Son"
        expected_phone = "+1234567890"
        expected_email = "contact@mail.com"
        emergency_contact = EmergencyContact(
            name=expected_name,
            relation=expected_relation,
            phone=expected_phone,
            email=expected_email,
            senior_id=senior_user.user_id,
        )
        db.session.add(emergency_contact)
        db.session.commit()

        saved_contact = EmergencyContact.query.filter_by(name=expected_name).first()
        assert saved_contact is not None
        assert saved_contact.name == expected_name
        assert saved_contact.relation == expected_relation
        assert saved_contact.phone == expected_phone
        assert saved_contact.email == expected_email
        assert saved_contact.senior_id == senior_user.user_id

    def test_generates_unique_ids_for_different_contacts(self, senior_user):
        old_contact = EmergencyContact(
            name="Old Contact",
            relation="Son",
            phone="+19999999999",
            email="old@mail.com",
            senior_id=senior_user.user_id,
        )
        new_contact = EmergencyContact(
            name="New Contact",
            relation="Daughter",
            phone="+19555555",
            email="new@mail.com",
            senior_id=senior_user.user_id
        )
        db.session.add_all([old_contact, new_contact])
        db.session.commit()

        assert old_contact.contact_id != new_contact.contact_id
        assert uuid.UUID(old_contact.contact_id)
        assert uuid.UUID(new_contact.contact_id)


class TestEmergencyContactsAPIAuthentication:

    #Response code 200 for GET
    def test_get_contacts_requires_authentication1(self, client, auth_headers):
        response = client.get("/api/v1/emergency-contacts", headers=auth_headers)
        assert response.status_code == 200


class TestEmergencyContactsAPI:

    #Response code 201 for POST
    def test_create_emergency_contact_api(self, client, auth_headers):
        response = client.post(
            "/api/v1/emergency-contacts",
            headers=auth_headers,
            json={
                "name": "Dummy Contact",
                "relation": "Friend",
                "phone": "+1234567890",
            },
        )
        data = response.get_json()
        assert response.status_code == 201
        #assert data["message"] == "Emergency Contact added"

    #Response code 400 for POST
    def test_create_emergency_contact_empty_json_body(self, client, auth_headers):
        response = client.post(
            "/api/v1/emergency-contacts",
            headers={
                **auth_headers,
                "Content-Type": "application/json",
            },
            data=""  # empty string with JSON header
        )
        assert response.status_code == 422


    #Response code 422 for POST
    def test_create_emergency_contact_with_missing_field_api(self, client, auth_headers):
        response = client.post(
            "/api/v1/emergency-contacts",
            headers=auth_headers,
            json={
                "name": "Dummy Provider",
                "relation": "Friend",
            },
        )
        data = response.get_json()
        assert response.status_code == 422

    
    #Response code 200 for GET using id
    def test_get_emergency_contact_with_id_api(self, client, auth_headers, sample_emergency_contact):
        contact_id = sample_emergency_contact.contact_id
        response = client.get(
            f"/api/v1/emergency-contacts/{contact_id}",
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 200

    #Response code 404 for GET using id
    def test_get_emergency_contact_with_wrong_id_api(self, client, auth_headers):
        contact_id = str(uuid.uuid4())
        response = client.get(
            f"/api/v1/emergency-contacts/{contact_id}",
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 404

    # Response code 200 for DELETE
    def test_delete_emergency_contact_api(self, client, auth_headers, sample_emergency_contact):
        contact_id = sample_emergency_contact.contact_id
        response = client.delete(
            f"/api/v1/emergency-contacts/{contact_id}",
                headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 200

    # Response code 400 for DELETE
    def test_delete_emergency_contact_with_wrong_id_api(self, client, auth_headers):
        contact_id = str(uuid.uuid4())
        response = client.delete(
            f"/api/v1/emergency-contacts/{contact_id}",
                headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 400



#Fixtures for Authentication Headers
@pytest.fixture
def auth2_headers(client, caregiver_user, senior_user):
    # Ensure assignment is created first
    assignment = CaregiverAssignment(
        caregiver_id=caregiver_user.user_id,
        senior_id=senior_user.user_id,
    )
    db.session.add(assignment)
    db.session.commit()

    # Now create token
    with client.application.app_context():
        access_token = create_access_token(
            identity=caregiver_user.user_id,
            additional_claims={"roles": [role.name for role in caregiver_user.roles]},
        )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def auth3_headers(client, provider_user):
    with client.application.app_context():
        access_token = create_access_token(
            identity=provider_user.user_id,
            additional_claims={"roles": [role.name for role in provider_user.roles]},
        )
    return {"Authorization": f"Bearer {access_token}"}