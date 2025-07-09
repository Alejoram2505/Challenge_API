import pytest
from app.main import db, create_app
from app.services.config_service import save_mock_config, get_all_mock_configs, delete_mock_config

@pytest.fixture
def app_context():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_save_and_get_mock(app_context):
    data = {
        "path": "/unit-test",
        "method": "GET",
        "query_params": {},
        "body_params": {},
        "headers": {},
        "response_status": 200,
        "response_body": {"msg": "ok"},
        "content_type": "application/json",
        "delay_ms": 0
    }

    success, mock_id = save_mock_config(data)
    assert success
    mocks = get_all_mock_configs()
    assert len(mocks) == 1
    assert mocks[0]["path"] == "/unit-test"

def test_delete_mock_config(app_context):
    # Crear
    data = {
        "path": "/to-delete",
        "method": "POST",
        "query_params": {},
        "body_params": {},
        "headers": {},
        "response_status": 201,
        "response_body": {"deleted": False},
        "content_type": "application/json",
        "delay_ms": 100
    }
    success, mock_id = save_mock_config(data)
    assert success

    # Eliminar
    deleted, msg = delete_mock_config(mock_id)
    assert deleted
    assert "eliminado correctamente" in msg
