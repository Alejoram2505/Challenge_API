from app.models.mock_config import MockConfig
from app.main import db

def save_mock_config(data):
    try:
        mock = MockConfig(
            path=data["path"],
            method=data["method"],
            query_params=data.get("query_params", {}),
            body_params=data.get("body_params", {}),
            headers=data.get("headers", {}),
            response_status=data.get("response_status", 200),
            response_body=data.get("response_body", {}),
            content_type=data.get("content_type", "application/json"),
            delay_ms=data.get("delay_ms", 0),
        )
        db.session.add(mock)
        db.session.commit()
        return True, mock.id
    except Exception as e:
        return False, str(e)

def get_all_mock_configs():
    configs = MockConfig.query.order_by(MockConfig.id.desc()).all()
    return [serialize_mock_config(c) for c in configs]

def serialize_mock_config(config):
    return {
        "id": config.id,
        "path": config.path,
        "method": config.method,
        "query_params": config.query_params,
        "body_params": config.body_params,
        "headers": config.headers,
        "response_status": config.response_status,
        "response_body": config.response_body,
        "content_type": config.content_type,
        "delay_ms": config.delay_ms,
        "created_at": config.created_at.isoformat()
    }

def delete_mock_config(config_id):
    config = db.session.get(MockConfig, config_id)
    if not config:
        return False, f"No se encontró mock con ID {config_id}"

    db.session.delete(config)
    db.session.commit()
    return True, f"Mock con ID {config_id} eliminado correctamente"
