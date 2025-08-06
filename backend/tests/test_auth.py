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
                "username": "testuser",
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

    def test_signup_duplicate_user(self, client, db_session):
        # First signup
        client.post(
            "/api/v1/auth/signup",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "role": "caregiver",
            },
        )

        # Try signing up again with same username/email
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "role": "caregiver",
            },
        )

        assert response.status_code == 409
        assert response.get_json()["message"] == "Username or email already exists"

    def test_signup_invalid_role(self, client, db_session):
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "username": "badroleuser",
                "email": "badrole@example.com",
                "password": "password123",
                "role": "alien",  # Not a valid role
            },
        )

        assert response.status_code == 400
        assert response.get_json()["message"] == "Invalid role specified"

    def test_login_success(self, client, db_session):
        # First signup
        client.post(
            "/api/v1/auth/signup",
            json={
                "username": "loginuser",
                "email": "login@example.com",
                "password": "mypassword",
                "role": "senior_citizen",
            },
        )

        # Then login
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "loginuser", "password": "mypassword"},
        )

        assert response.status_code == 200
        assert "access_token" in response.get_json()

    def test_login_wrong_password(self, client, db_session):
        # Signup with known password
        client.post(
            "/api/v1/auth/signup",
            json={
                "username": "wrongpass",
                "email": "wrongpass@example.com",
                "password": "rightpassword",
                "role": "SeniorCitizen",
            },
        )

        # Try logging in with wrong password
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "wrongpass", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        assert response.get_json()["message"] == "Bad username or password"

    def test_login_nonexistent_user(self, client):
        # Attempt login for a non-existent user
        response = client.post(
            "/api/v1/auth/login", json={"username": "ghost", "password": "nope"}
        )

        assert response.status_code == 401
        assert response.get_json()["message"] == "Bad username or password"
