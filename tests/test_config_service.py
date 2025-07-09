from app.services.config_service import save_mock_config, get_all_mock_configs

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
