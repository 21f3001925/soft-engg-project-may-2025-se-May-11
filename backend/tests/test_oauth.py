import pytest
from flask import current_app, redirect
from flask_jwt_extended import decode_token
from urllib.parse import urlparse, parse_qs
from models import User, Role, db


@pytest.mark.usefixtures("app", "client")
class TestOAuthGoogleLogin:
    def test_google_login_redirects_to_google(self, client, mocker):
        # Patch url_for exactly where it's used
        mocker.patch("routes.oauth.url_for", return_value="http://mocked-callback-url")

        # Mock the Google OAuth client
        mock_google = mocker.MagicMock()
        mock_google.authorize_redirect.return_value = redirect(
            "http://mocked-google-auth-url"
        )

        # Patch current_app.oauth
        mock_oauth = mocker.MagicMock()
        mock_oauth.google = mock_google
        mocker.patch.object(current_app, "oauth", mock_oauth)

        # Act
        response = client.get("/api/v1/oauth/google/login")

        # Assert
        assert response.status_code == 302
        assert response.location == "http://mocked-google-auth-url"
        mock_google.authorize_redirect.assert_called_once_with(
            "http://mocked-callback-url"
        )


@pytest.mark.usefixtures("app", "client")
class TestOAuthGoogleCallback:
    def test_registers_new_user_and_redirects_with_token(self, client, app, mocker):
        with app.app_context():
            email = "newuser@example.com"
            username = "New User"

            # Ensure caregiver role exists
            role = Role.query.filter_by(name="caregiver").first()
            if not role:
                role = Role(name="caregiver", description="Default caregiver role")
                db.session.add(role)
                db.session.commit()

            # Clean up any existing user
            User.query.filter_by(email=email).delete()
            db.session.commit()

            # Patch Google OAuth token response
            mock_token = {"userinfo": {"email": email, "name": username}}
            mock_google = mocker.MagicMock()
            mock_google.authorize_access_token.return_value = mock_token

            mock_oauth = mocker.MagicMock()
            mock_oauth.google = mock_google
            mocker.patch.object(current_app, "oauth", mock_oauth)

            # Patch FRONTEND_URL
            mocker.patch.dict(
                "os.environ", {"FRONTEND_URL": "http://localhost:3000/oauth/callback"}
            )

            #  Patch User init to avoid password=None issue
            original_user_init = User.__init__

            def patched_user_init(self, username, email, password=None, **kwargs):
                if password is None:
                    password = "test1234"  # dummy password
                original_user_init(
                    self, username=username, email=email, password=password, **kwargs
                )

            mocker.patch("models.User.__init__", patched_user_init)

            # Call endpoint (real redirect will occur)
            response = client.get(
                "/api/v1/oauth/google/callback", follow_redirects=False
            )

            #  Assert redirect response
            assert response.status_code == 302
            assert "Location" in response.headers

            redirect_url = response.headers["Location"]
            assert redirect_url.startswith(
                "http://localhost:3000/oauth/callback?token="
            )

            #  Assert user was created
            user = User.query.filter_by(email=email).first()
            assert user is not None
            assert user.username == username

            #  Assert token is valid
            token = parse_qs(urlparse(redirect_url).query).get("token", [None])[0]
            assert token is not None
            decoded = decode_token(token)
            assert decoded["sub"] == str(user.user_id)

    def test_existing_user_is_logged_in_and_redirects_with_token(
        self, client, app, mocker
    ):
        with app.app_context():
            email = "existinguser@example.com"
            username = "Existing User"

            # Ensure caregiver role exists
            role = Role.query.filter_by(name="caregiver").first()
            if not role:
                role = Role(name="caregiver", description="Default caregiver role")
                db.session.add(role)
                db.session.commit()

            # Pre-create user
            user = User(username=username, email=email, password="dummy123")
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()

            # Mock Google OAuth token with same user
            mock_token = {"userinfo": {"email": email, "name": username}}
            mock_google = mocker.MagicMock()
            mock_google.authorize_access_token.return_value = mock_token

            mock_oauth = mocker.MagicMock()
            mock_oauth.google = mock_google
            mocker.patch.object(current_app, "oauth", mock_oauth)

            # Patch FRONTEND_URL
            mocker.patch.dict(
                "os.environ", {"FRONTEND_URL": "http://localhost:3000/oauth/callback"}
            )

            response = client.get(
                "/api/v1/oauth/google/callback", follow_redirects=False
            )
            assert response.status_code == 302
            redirect_url = response.headers["Location"]
            assert redirect_url.startswith(
                "http://localhost:3000/oauth/callback?token="
            )

            # Token validation
            token = parse_qs(urlparse(redirect_url).query).get("token", [None])[0]
            assert token is not None
            decoded = decode_token(token)
            assert decoded["sub"] == str(user.user_id)

    def test_returns_401_if_userinfo_missing(self, client, app, mocker):
        with app.app_context():
            # Simulate OAuth callback without userinfo
            mock_google = mocker.MagicMock()
            mock_google.authorize_access_token.return_value = {}

            mock_oauth = mocker.MagicMock()
            mock_oauth.google = mock_google
            mocker.patch.object(current_app, "oauth", mock_oauth)

            response = client.get("/api/v1/oauth/google/callback")
            assert response.status_code == 401
            assert response.json["message"] == "Failed to get user info from Google."
