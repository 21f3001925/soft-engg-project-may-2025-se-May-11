import pytest
from app_factory import create_app
from extensions import db
from test_config import TestConfig


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
