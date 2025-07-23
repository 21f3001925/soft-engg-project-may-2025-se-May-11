import pytest
from datetime import datetime, timezone
import bcrypt
from app_factory import create_app
from extensions import db
from test_config import TestConfig
from models import User, Role, Medication


@pytest.fixture(scope="session")
def app():
    test_app = create_app(config_class=TestConfig)

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        db.session.execute(db.text("DELETE FROM medication"))
        db.session.execute(db.text("DELETE FROM roles_users"))
        db.session.execute(db.text("DELETE FROM user"))
        db.session.execute(db.text("DELETE FROM role"))
        db.session.commit()
        yield
        db.session.rollback()


@pytest.fixture
def senior_user():
    role = Role(name="senior_citizen", description="senior_citizen role")
    db.session.add(role)
    db.session.flush()

    hashed_pw = bcrypt.hashpw("TestPassword123!".encode(), bcrypt.gensalt()).decode()
    user = User(
        username="test_senior",
        email="test_senior@test.com",
        password=hashed_pw,
        phone_number="+1234567890",
        name="Test Senior",
    )
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def caregiver_user():
    role = Role(name="caregiver", description="caregiver role")
    db.session.add(role)
    db.session.flush()

    hashed_pw = bcrypt.hashpw("TestPassword123!".encode(), bcrypt.gensalt()).decode()
    user = User(
        username="test_caregiver",
        email="test_caregiver@test.com",
        password=hashed_pw,
        phone_number="+1234567890",
        name="Test Caregiver",
    )
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_headers(client, senior_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": senior_user.username, "password": "TestPassword123!"},
    )
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_medication(senior_user):
    medication = Medication(
        name="Sample Medication",
        dosage="10mg",
        time=datetime.now(timezone.utc),
        isTaken=False,
        senior_id=senior_user.user_id,
    )
    db.session.add(medication)
    db.session.commit()
    return medication
