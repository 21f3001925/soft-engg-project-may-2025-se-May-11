# test_events.py
from datetime import datetime, timezone
import uuid


class TestDatabaseConfiguration:

    def test_uses_in_memory_database(self, app):
        with app.app_context():
            assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
            assert app.config["TESTING"] is True


class TestEventAPI:

    def test_get_all_events(self, client, provider_auth_headers):
        response = client.get("/api/v1/events", headers=provider_auth_headers)
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)

    def test_create_event(self, client, provider_user, provider_auth_headers):
        response = client.post(
            "/api/v1/events",
            json={
                "name": "Yoga Class",
                "date_time": datetime(
                    2025, 7, 25, 10, 0, 0, tzinfo=timezone.utc
                ).isoformat(),
                "location": "Community Center",
                "description": "Weekly yoga class for all levels.",
                "service_provider_id": provider_user.user_id,
            },
            headers=provider_auth_headers,
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Yoga Class"
        assert data["location"] == "Community Center"
        assert data["service_provider_id"] == provider_user.user_id

    def test_get_event_by_id(
        self, client, provider_auth_headers, sample_event, auth_headers
    ):
        event_id = sample_event.event_id
        response = client.get(
            f"/api/v1/events/{event_id}", headers=provider_auth_headers
        )
        assert response.status_code == 200

    def test_get_event_by_invalid_id(
        self, client, provider_auth_headers, sample_event, auth_headers
    ):
        random_id = str(uuid.uuid4())
        response = client.get(
            f"/api/v1/events/{random_id}", headers=provider_auth_headers
        )
        assert response.status_code == 404

    def test_update_event(
        self,
        client,
        provider_auth_headers,
        sample_event,
        auth_headers,
    ):
        event_id = sample_event.event_id
        response = client.put(
            f"/api/v1/events/{event_id}",
            json={"location": "Updated Hall"},
            headers=provider_auth_headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["location"] == "Updated Hall"

    def test_delete_event(
        self, client, provider_auth_headers, sample_event, auth_headers
    ):
        event_id = sample_event.event_id
        response = client.delete(
            f"/api/v1/events/{event_id}",
            headers=provider_auth_headers,
        )
        assert response.status_code == 204

    def test_delete_event_invalid_id(
        self, client, provider_auth_headers, sample_event, auth_headers
    ):
        random_id = str(uuid.uuid4())
        response = client.delete(
            f"/api/v1/events/{random_id}", headers=provider_auth_headers
        )
        assert response.status_code == 404

    def test_create_event_missing_fields(
        self, client, provider_auth_headers, provider_user
    ):
        response = client.post(
            "/api/v1/events",
            json={
                "date_time": datetime(
                    2025, 7, 25, 10, 0, 0, tzinfo=timezone.utc
                ).isoformat(),
                "location": "Center",
                "service_provider_id": provider_user.user_id,
            },
            headers=provider_auth_headers,
        )
        assert response.status_code == 422  # name is missing

    def test_authentication_required(self, client):
        response = client.get("/api/v1/events")
        assert response.status_code == 401

    def test_authorization_required(self, client, auth_headers):
        # auth_headers uses senior_user, who is not a service_provider
        response = client.get("/api/v1/events", headers=auth_headers)
        assert response.status_code == 200  # or custom unauthorized message
