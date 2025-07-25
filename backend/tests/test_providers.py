import uuid
import pytest
from flask_jwt_extended import create_access_token

from models import User, db, ServiceProvider


class TestDatabaseConfiguration:

    def test_uses_in_memory_database(self, app):
        with app.app_context():
            assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
            assert app.config["TESTING"] is True


class TestServiceProviderModel:

    def test_creates_service_provider_with_all_fields(self):
        expected_name = "Service_Manager1"
        expected_contact_email = "xyz@gmail.com"
        expected_phone_number = "+1234567890"
        expected_services_offered = "Yoga"
        service_provider = ServiceProvider(
            name=expected_name,
            contact_email=expected_contact_email,
            phone_number=expected_phone_number,
            services_offered=expected_services_offered,
        )
        db.session.add(service_provider)
        db.session.commit()

        saved_provider = ServiceProvider.query.filter_by(name=expected_name).first()
        assert saved_provider is not None
        assert saved_provider.name == expected_name
        assert saved_provider.contact_email == expected_contact_email
        assert saved_provider.phone_number == expected_phone_number
        assert saved_provider.services_offered == expected_services_offered


    def test_generates_unique_ids_for_different_providers(self):
        old_provider = ServiceProvider(
            name="Old Provider",
            contact_email="old@mail.com",
            phone_number="+19999999999",
            services_offered="Old Services",
        )
        new_provider = ServiceProvider(
            name="New Provider",
            contact_email="new@mail.com",
            phone_number="+19555555",
            services_offered="New Services",
        )
        db.session.add_all([old_provider, new_provider])
        db.session.commit()

        assert old_provider.service_provider_id != new_provider.service_provider_id
        assert uuid.UUID(old_provider.service_provider_id)
        assert uuid.UUID(new_provider.service_provider_id)


class TestUserRoleAssignment:

    def test_provider_user_has_correct_role(self, provider_user):
        found_user = User.query.filter_by(username=provider_user.username).first()

        assert found_user is not None
        assert len(found_user.roles) == 1
        assert found_user.roles[0].name == "service_provider"


class TestProvidersAPIAuthentication:

    def test_get_providers_requires_authentication1(self, client):
        response = client.get("/api/v1/providers")
        assert response.status_code == 401

    def test_get_providers_requires_authentication2(self, client, auth3_headers):
        response = client.get("/api/v1/providers", headers=auth3_headers)
        assert response.status_code == 200

class TestProvidersAPI:

    def test_create_service_provider_with_senior_citizen_api(self, client, auth_headers):
        response = client.post(
            "/api/v1/providers",
            headers=auth_headers,
            json={
                "name": "Dummy Provider",
                "contact_email": "dummymail@mail.com",
                "phone_number": "+1234567890",
                "services_offered": "Pain relief",
            },
        )
        data = response.get_json()
        assert response.status_code == 201
        #assert data["message"] == "Provider added"

    def test_create_service_provider_with_caregiver_api(self, client, auth2_headers):
        response = client.post(
            "/api/v1/providers",
            headers=auth2_headers,
            json={
                "name": "Dummy Provider",
                "contact_email": "dummymail@mail.com",
                "phone_number": "+1234567890",
                "services_offered": "Pain relief",
            },
        )
        data = response.get_json()
        assert response.status_code == 403
        #assert data["message"] == "Provider added"
    
    def test_create_service_provider_with_missing_values_api(self, client, auth3_headers):
        response = client.post(
            "/api/v1/providers",
            headers=auth3_headers,
            json={
                "name": "Dummy Provider",
                "phone_number": "+1234567890",
                "services_offered": "Pain relief",
            },
        )
        data = response.get_json()
        assert response.status_code == 422
        #assert data["message"] == "Provider added"

    def test_create_service_provider_with_caregiver_api(self, client, auth2_headers):
        response = client.post(
            "/api/v1/providers",
            headers=auth2_headers,
            json={
                "name": "Dummy Provider",
                "contact_email": "dummymail@mail.com",
                "phone_number": "+1234567890",
                "services_offered": "Pain relief",
            },
        )
        data = response.get_json()
        assert response.status_code == 403
        #assert data["message"] == "Provider added"

    def test_get_all_service_provider_info_api(self, client, auth_headers):
        response = client.get(
            "/api/v1/providers",
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 200

    def test_get_service_provider_info_with_correct_id_api(self, client, auth3_headers, sample_provider):
        prod_id = sample_provider.service_provider_id
        response = client.get(
            f"/api/v1/providers/{prod_id}",
            headers=auth3_headers,
        )
        data = response.get_json()
        assert response.status_code == 200

    def test_get_service_provider_info_with_wrong_id_api(self, client, auth3_headers):
        prod_id = str(uuid.uuid4())
        response = client.get(
            f"/api/v1/providers/{prod_id}",
            headers=auth3_headers,
        )
        data = response.get_json()
        assert response.status_code == 404

    def test_edit_service_provider_info_with_correct_id_api(self, client, auth3_headers, sample_provider):
        prod_id = sample_provider.service_provider_id
        response = client.put(
            f"/api/v1/providers/{prod_id}",
            headers=auth3_headers,
            json={
                "name": "Updated Provider",
                "contact_email": "updated@example.com",
                "phone_number": "+1234567890",
                "services_offered": "Updated Services",
            }
        )
        data = response.get_json()
        assert response.status_code == 200

    def test_edit_service_provider_info_with_id_using_wrong_data_api(self, client, auth3_headers, sample_provider):
        prod_id = sample_provider.service_provider_id
        response = client.put(
            f"/api/v1/providers/{prod_id}",
            headers=auth3_headers,
            json={
                "name": "Updated Provider",
                "contact_email": "updated@example.com",
                "phone_number": "+1234567890",
                "services_offered": "Updated Services",
                "address": "123 Main St"  # Extra field not expected
            }
        )
        data = response.get_json()
        assert response.status_code == 422

    def test_edit_service_provider_info_with_wrong_id_api(self, client, auth3_headers):
        prod_id = str(uuid.uuid4())
        response = client.put(
            f"/api/v1/providers/{prod_id}",
            headers=auth3_headers,
            json={
                "name": "Updated Provider",
                "contact_email": "updated@example.com",
                "phone_number": "+1234567890",
                "services_offered": "Updated Services",
            }
        )
        data = response.get_json()
        assert response.status_code == 404

    def test_delete_service_provider_info_with_correct_id_api(self, client, auth3_headers, sample_provider):
        prod_id = sample_provider.service_provider_id
        response = client.delete(
            f"/api/v1/providers/{prod_id}",
            headers=auth3_headers,
        )
        #data = response.get_json()
        assert response.status_code == 204

    def test_delete_service_provider_info_with_wrong_id_api(self, client, auth3_headers):
        prod_id = str(uuid.uuid4())
        response = client.delete(
            f"/api/v1/providers/{prod_id}",
            headers=auth3_headers,
        )
        data = response.get_json()
        assert response.status_code == 404

    def test_get_all_service_info_with_correct_provider_id_api(self, client, auth3_headers, sample_provider):
        prod_id = sample_provider.service_provider_id
        response = client.get(
            f"/api/v1/providers/{prod_id}/events",
            headers=auth3_headers,
        )
        data = response.get_json()
        assert response.status_code == 200

    def test_get_all_service_info_with_wrong_provider_id_api(self, client, auth3_headers):
        prod_id = str(uuid.uuid4())
        response = client.get(
            f"/api/v1/providers/{prod_id}/events",
            headers=auth3_headers,
        )
        data = response.get_json()
        assert response.status_code == 404


#Fixtures for Authentication Headers
@pytest.fixture
def auth2_headers(client, caregiver_user):
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
