import pytest
from app.main import create_app, db
from app.test_config import TestConfig

@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def app_context(app):
    with app.app_context():
        yield
