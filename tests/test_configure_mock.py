def test_configure_mock_post(client):
    data = {
        "path": "/configure-test",
        "method": "GET",
        "query_params": {},
        "body_params": {},
        "headers": {},
        "response_status": 200,
        "response_body": {"msg": "works"},
        "content_type": "application/json",
        "delay_ms": 0
    }

    response = client.post("/configure-mock", json=data)
    assert response.status_code == 201
    assert response.json["message"] == "Configuración registrada"

def test_list_mocks(client):
    response = client.get("/configure-mock")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_delete_mock(client):
    # Crear mock primero
    data = {
        "path": "/delete-test",
        "method": "GET",
        "query_params": {},
        "body_params": {},
        "headers": {},
        "response_status": 200,
        "response_body": {"msg": "bye"},
        "content_type": "application/json",
        "delay_ms": 0
    }

    post_response = client.post("/configure-mock", json=data)
    assert post_response.status_code == 201
    mock_id = post_response.json["id"]

    # Eliminar
    delete_response = client.delete(f"/configure-mock/{mock_id}")
    assert delete_response.status_code == 200
