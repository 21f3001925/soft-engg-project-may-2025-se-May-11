import uuid

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

    def test_applies_default_values_when_not_specified(self):
        dummy_provider = ServiceProvider(
            name="Dummy Provider",
            contact_email="xyz@mail.com",
            phone_number="+19999999999",
            services_offered="Dummy Services",
        )
        db.session.add(dummy_provider)
        db.session.commit()

        assert dummy_provider.service_provider_id is not None

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

    def test_get_providers_requires_authentication(self, client):
        response = client.get("/api/v1/providers")
        assert response.status_code == 401
