def test_generic_mock_response(client):
    mock_data = {
        "path": "/mock-test",
        "method": "GET",
        "query_params": {},
        "body_params": {},
        "headers": {},
        "response_status": 200,
        "response_body": {"msg": "funciona"},
        "content_type": "application/json",
        "delay_ms": 0
    }
    post_res = client.post("/configure-mock", json=mock_data)
    assert post_res.status_code == 201

    response = client.get("/mock-test")
    assert response.status_code == 200
    assert response.json == {"msg": "funciona"}

def test_generic_mock_with_query_params(client):
    mock_data = {
        "path": "/query-test",
        "method": "GET",
        "query_params": {"user": "admin"},
        "body_params": {},
        "headers": {},
        "response_status": 200,
        "response_body": {"msg": "admin access"},
        "content_type": "application/json",
        "delay_ms": 0
    }
    client.post("/configure-mock", json=mock_data)

    res_ok = client.get("/query-test?user=admin")
    assert res_ok.status_code == 200
    assert res_ok.json == {"msg": "admin access"}

    res_fail = client.get("/query-test?user=wrong")
    assert res_fail.status_code == 404

def test_generic_mock_with_headers(client):
    mock_data = {
        "path": "/header-test",
        "method": "GET",
        "query_params": {},
        "body_params": {},
        "headers": {"X-Test": "123"},
        "response_status": 200,
        "response_body": {"msg": "header ok"},
        "content_type": "application/json",
        "delay_ms": 0
    }
    client.post("/configure-mock", json=mock_data)

    res_ok = client.get("/header-test", headers={"X-Test": "123"})
    assert res_ok.status_code == 200
    assert res_ok.json == {"msg": "header ok"}

    res_fail = client.get("/header-test", headers={"X-Test": "wrong"})
    assert res_fail.status_code == 404
