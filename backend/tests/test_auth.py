import pytest
from flask_jwt_extended import decode_token
from models import Role


# Automatically create roles for all tests in this class
@pytest.fixture
def create_roles(db_session):
    """Create required roles in the database."""
    roles = ["caregiver", "senior_citizen", "service_provider"]
    for role in roles:
        db_session.add(Role(name=role))
    db_session.commit()


@pytest.mark.usefixtures("create_roles")
class TestAuth:

    def test_signup_success(self, client, db_session):
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "test@example.com",
                "password": "password123",
                "role": "caregiver",
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert "access_token" in data

        token_data = decode_token(data["access_token"])
        assert "sub" in token_data  # user_id is stored in `sub`

    def test_signup_duplicate_email(self, client, db_session):
        # First signup
        client.post(
            "/api/v1/auth/signup",
            json={
                "email": "test@example.com",
                "password": "password123",
                "role": "caregiver",
            },
        )

        # Try signing up again with same email
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "test@example.com",
                "password": "password123",
                "role": "caregiver",
            },
        )

        assert response.status_code == 409
        assert response.get_json()["message"] == "Email already exists"

    def test_signup_invalid_role(self, client, db_session):
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "badrole@example.com",
                "password": "password123",
                "role": "alien",  # Not a valid role
            },
        )

        assert response.status_code == 400
        assert response.get_json()["message"] == "Invalid role specified"

    def test_login_success_with_email(self, client, db_session):
        # First signup
        client.post(
            "/api/v1/auth/signup",
            json={
                "email": "login@example.com",
                "password": "mypassword",
                "role": "senior_citizen",
            },
        )

        # Then login with email
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "login@example.com", "password": "mypassword"},
        )

        assert response.status_code == 200
        assert "access_token" in response.get_json()

    def test_login_success_with_phone(self, client, db_session):
        # Signup using phone only
        client.post(
            "/api/v1/auth/signup",
            json={
                "phone_number": "+919876543210",
                "password": "mypassword",
                "role": "senior_citizen",
            },
        )

        # Then login with phone
        response = client.post(
            "/api/v1/auth/login",
            json={"phone_number": "+919876543210", "password": "mypassword"},
        )

        assert response.status_code == 200
        assert "access_token" in response.get_json()

    def test_login_wrong_password(self, client, db_session):
        # Signup with known password
        client.post(
            "/api/v1/auth/signup",
            json={
                "email": "wrongpass@example.com",
                "password": "rightpassword",
                "role": "senior_citizen",
            },
        )

        # Try logging in with wrong password
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "wrongpass@example.com", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        assert response.get_json()["message"] == "Bad email or password"

    def test_signup_duplicate_phone(self, client, db_session):
        # First signup with phone
        client.post(
            "/api/v1/auth/signup",
            json={
                "phone_number": "+919876543210",
                "password": "password123",
                "role": "caregiver",
            },
        )

        # Duplicate with same phone
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "phone_number": "+919876543210",
                "password": "password123",
                "role": "caregiver",
            },
        )

        assert response.status_code == 409
        assert response.get_json()["message"] == "Phone number already exists"

    def test_login_nonexistent_user(self, client):
        # Attempt login for a non-existent user
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "ghost@example.com", "password": "nope"},
        )

        assert response.status_code == 401
        assert response.get_json()["message"] == "Bad email or password"
