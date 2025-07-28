import uuid
import pytest
from datetime import datetime, timedelta, timezone
import bcrypt
from app_factory import create_app
from extensions import db
from test_config import TestConfig
from models import Appointment, User, Role, Medication
from flask_jwt_extended import create_access_token


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
        db.session.rollback()  # Reset any broken session at the start

        # Clean the tables in correct dependency order
        db.session.execute(db.text("DELETE FROM medication"))
        db.session.execute(db.text("DELETE FROM appointment"))
        db.session.execute(db.text("DELETE FROM roles_users"))
        db.session.execute(db.text("DELETE FROM user"))
        db.session.execute(db.text("DELETE FROM role"))
        db.session.commit()

        yield  # run the test

        db.session.rollback()  # Ensure cleanup after test if needed


@pytest.fixture
def senior_user():
    role = Role.query.filter_by(name="senior_citizen").first()
    if not role:
        role = Role(name="senior_citizen")
        db.session.add(role)
        db.session.flush()

    user = User(
        username="test_senior",
        email="test_senior@example.com",
        password=bcrypt.hashpw("TestPassword123!".encode(), bcrypt.gensalt()).decode(),
    )
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def caregiver_user():
    role = Role.query.filter_by(name="caregiver").first()
    if not role:
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
def provider_user():
    role = Role(name="service_provider", description="service_provider role")
    db.session.add(role)
    db.session.flush()

    hashed_pw = bcrypt.hashpw("TestPassword123!".encode(), bcrypt.gensalt()).decode()
    user = User(
        username="test_provider",
        email="test_provider@test.com",
        password=hashed_pw,
        phone_number="+1234567890",
        name="Test Provider",
    )
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    # provider_id = user.user_id
    return user


@pytest.fixture
def auth_headers(client, senior_user):
    with client.application.app_context():
        access_token = create_access_token(
            identity=senior_user.user_id,
            additional_claims={"roles": [role.name for role in senior_user.roles]},
        )
    return {"Authorization": f"Bearer {access_token}"}


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


@pytest.fixture
def sample_appointment(senior_user):
    """Create a sample appointment for testing"""
    appointment = Appointment(
        appointment_id=str(uuid.uuid4()),
        title="Sample Appointment",
        date_time=datetime.now(timezone.utc) + timedelta(days=1),
        location="Sample Location",
        senior_id=senior_user.user_id,
    )
    db.session.add(appointment)
    db.session.flush()
    db.session.commit()
    return appointment


@pytest.fixture
def db_session(app):
    """Returns a database session object."""
    with app.app_context():
        yield db.session


@pytest.fixture
def caregiver_auth_headers(caregiver_user):
    """Create auth headers for caregiver"""
    token = create_access_token(identity=caregiver_user.user_id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_user_auth_headers(other_senior_user):
    """Create auth headers for other senior user"""
    token = create_access_token(
        identity=other_senior_user.user_id,
        additional_claims={"roles": [role.name for role in other_senior_user.roles]},
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_senior_user():
    role = Role.query.filter_by(name="senior_citizen").first()
    if not role:
        role = Role(name="senior_citizen", description="senior_citizen role")
        db.session.add(role)
        db.session.flush()

    hashed_pw = bcrypt.hashpw(
        "OtherTestPassword123!".encode(), bcrypt.gensalt()
    ).decode()
    user = User(
        username="other_senior",
        email="other_senior@test.com",
        password=hashed_pw,
        phone_number="+1987654321",
        name="Other Senior",
    )
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    return user
