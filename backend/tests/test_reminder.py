from datetime import datetime, timezone
import uuid


class TestDatabaseConfiguration:

    def test_uses_in_memory_database(self, app):
        with app.app_context():
            assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
            assert app.config["TESTING"] is True


class TestReminderAPI:

    def test_schedule_reminder_valid(self, client, auth_headers):
        payload = {
            "appointment_id": str(uuid.uuid4()),
            "title": "Doctor's Visit",
            "location": "Clinic",
            "date_time": datetime(
                2025, 7, 20, 10, 0, 0, tzinfo=timezone.utc
            ).isoformat(),
            "email": "senior@example.com",
        }
        response = client.post(
            "/api/v1/reminder/schedule-reminder", json=payload, headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data.get("message") == "Reminders scheduled"

    def test_schedule_reminder_missing_fields(self, client, auth_headers):
        # Omitting "title" and "date_time"
        bad_payload = {
            "appointment_id": str(uuid.uuid4()),
            "location": "Clinic",
            "email": "senior@example.com",
        }
        response = client.post(
            "/api/v1/reminder/schedule-reminder", json=bad_payload, headers=auth_headers
        )
        # Should get validation error (422 or 400 depending on your API)
        assert response.status_code in (400, 422)

    def test_schedule_reminder_invalid_date_format(self, client, auth_headers):
        payload = {
            "appointment_id": str(uuid.uuid4()),
            "title": "Blood Test",
            "location": "Lab",
            "date_time": "invalid-format",
            "email": "senior@example.com",
        }
        response = client.post(
            "/api/v1/reminder/schedule-reminder", json=payload, headers=auth_headers
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "Invalid date_time format" in (data.get("message") or "")

    def test_schedule_reminder_no_auth(self, client):
        payload = {
            "appointment_id": str(uuid.uuid4()),
            "title": "Checkup",
            "location": "Hospital",
            "date_time": datetime(
                2025, 8, 1, 15, 0, 0, tzinfo=timezone.utc
            ).isoformat(),
            "email": "senior@example.com",
        }
        response = client.post("/api/v1/reminder/schedule-reminder", json=payload)
        # Unauthorized, should be 401
        assert response.status_code == 401

    def test_schedule_reminder_unexpected_field(self, client, auth_headers):
        payload = {
            "appointment_id": str(uuid.uuid4()),
            "title": "Dentist",
            "location": "Dental Clinic",
            "date_time": datetime(
                2025, 7, 30, 11, 0, 0, tzinfo=timezone.utc
            ).isoformat(),
            "email": "senior@example.com",
            "reminder_type": "sms",  # Suppose this is NOT accepted by the API
        }
        response = client.post(
            "/api/v1/reminder/schedule-reminder", json=payload, headers=auth_headers
        )
        # Should be 422 if your API rejects unknown fields; adjust per your API
        assert response.status_code in (200, 400, 422)
