import pytest
import json
from app.main import create_app, db
from app.models.mock_config import MockConfig

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_create_mock(client):
    data = {
        "path": "/test-mock",
        "method": "GET",
        "query_params": {},
        "body_params": {},
        "headers": {},
        "response_status": 200,
        "response_body": {"mensaje": "hola"},
        "content_type": "application/json",
        "delay_ms": 0
    }
    response = client.post("/configure-mock", json=data)
    assert response.status_code == 201

    json_data = response.get_json()
    assert json_data["message"] == "Configuración registrada"
    assert "id" in json_data

def test_get_mocks(client):
    # Crear un mock
    client.post("/configure-mock", json={
        "path": "/test",
        "method": "GET",
        "query_params": {},
        "body_params": {},
        "headers": {},
        "response_status": 200,
        "response_body": {"msg": "ok"},
        "content_type": "application/json",
        "delay_ms": 0
    })

    response = client.get("/configure-mock")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["path"] == "/test"

def test_delete_mock(client):
    # Crear mock
    post_res = client.post("/configure-mock", json={
        "path": "/delete-test",
        "method": "GET",
        "query_params": {},
        "body_params": {},
        "headers": {},
        "response_status": 200,
        "response_body": {"msg": "bye"},
        "content_type": "application/json",
        "delay_ms": 0
    })

    mock_id = post_res.get_json()["id"]

    # Eliminar mock
    del_res = client.delete(f"/configure-mock/{mock_id}")
    assert del_res.status_code == 200

    json_data = del_res.get_json()
    assert "eliminado correctamente" in json_data["message"]
