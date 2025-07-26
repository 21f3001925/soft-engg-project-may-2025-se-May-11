import uuid
import pytest
from flask_jwt_extended import create_access_token

from models import db, EmergencyContact


class TestEmergencyContactsAPIAuthentication:

    #Response code 200 for GET
    def test_post_emergency_requires_authentication1(self, client, auth_headers):
        response = client.post("/api/v1/emergency/trigger", headers=auth_headers)
        assert response.status_code == 200

    #Response code 401 for GET
    def test_post_emergency_requires_authentication2(self, client):
        response = client.post("/api/v1/emergency/trigger")
        assert response.status_code == 401