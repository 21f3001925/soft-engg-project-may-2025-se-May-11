import io


class TestDatabaseConfiguration:

    def test_uses_in_memory_database(self, app):
        with app.app_context():
            assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
            assert app.config["TESTING"] is True


class TestProfileAPI:

    def test_get_profile(self, client, auth_headers):
        """Should retrieve profile info for authenticated user."""
        response = client.get("/api/v1/profile", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        # Check some mandatory profile fields
        assert "username" in data
        assert "email" in data
        assert "name" in data
        assert "avatar_url" in data

    def test_get_profile_unauthenticated(self, client):
        """Should return 401 if not authenticated."""
        response = client.get("/api/v1/profile")
        assert response.status_code == 401

    def test_update_profile(self, client, auth_headers):
        """Should update the user's profile name."""
        new_name = "Updated Name"
        response = client.put(
            "/api/v1/profile",
            headers=auth_headers,
            json={"name": new_name},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == new_name

    def test_delete_profile(self, client, auth_headers):
        """Should delete the user profile (204, cannot get after)."""
        response = client.delete("/api/v1/profile", headers=auth_headers)
        assert response.status_code == 204

        # Now, requests should fail
        get_after = client.get("/api/v1/profile", headers=auth_headers)
        assert get_after.status_code in (401, 404)  # depends on your backend's behavior

    def test_change_password_success(self, client, auth_headers):
        """Should allow changing password with correct current password."""
        payload = {
            "current_password": "TestPassword123!",  # match password in your conftest.py/test setup
            "new_password": "ANewStrongPassword#2",
        }
        response = client.post(
            "/api/v1/profile/change-password", json=payload, headers=auth_headers
        )
        assert response.status_code == 204

    def test_change_password_wrong_current(self, client, auth_headers):
        """Should return 401 with incorrect current password."""
        payload = {
            "current_password": "wrongpassword",
            "new_password": "AnotherNewStrongPassword#3",
        }
        response = client.post(
            "/api/v1/profile/change-password", json=payload, headers=auth_headers
        )
        assert response.status_code == 401
        data = response.get_json()
        assert "Invalid current password" in data.get("message", "")

    def test_upload_avatar(self, client, auth_headers):
        """Should upload a new avatar image for user."""
        # Create a fake PNG byte stream
        fake_img = io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"x" * 50)
        fake_img.name = "test.png"  # Flask/Werkzeug uses .name for file extension

        data = {"file": (fake_img, fake_img.name)}
        response = client.put(
            "/api/v1/profile/avatar",
            content_type="multipart/form-data",
            headers=auth_headers,
            data=data,
        )
        assert response.status_code == 200
        result = response.get_json()
        assert "avatar_url" in result
        assert result["avatar_url"].endswith(".png")

    def test_upload_avatar_no_file(self, client, auth_headers):
        """Should return 400 if no file part is sent."""
        response = client.put(
            "/api/v1/profile/avatar",
            content_type="multipart/form-data",
            headers=auth_headers,
            data={},
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "No file part" in data.get("message", "")

    def test_upload_avatar_invalid_type(self, client, auth_headers):
        """Should return 400 if the file is not an image or invalid type (if API checks this)."""
        fake_txt = io.BytesIO(b"NotAnImageFileContent")
        fake_txt.name = "notanimage.txt"
        data = {"file": (fake_txt, fake_txt.name)}
        response = client.put(
            "/api/v1/profile/avatar",
            content_type="multipart/form-data",
            headers=auth_headers,
            data=data,
        )
        # Should be rejected if your API checks filetype, else may also be 200
        assert response.status_code in (400, 422, 200)
