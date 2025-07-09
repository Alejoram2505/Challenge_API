from app.models.mock_config import MockConfig
from app.utils.matching import match_value

def find_matching_mock(path, method, query, body, headers):
    candidates = MockConfig.query.filter_by(path=path, method=method).all()

    for config in candidates:
        if not all(match_value(config.query_params.get(k), query.get(k)) for k in config.query_params):
            continue
        if not all(match_value(config.body_params.get(k), body.get(k)) for k in config.body_params):
            continue
        if not all(match_value(config.headers.get(k), headers.get(k)) for k in config.headers):
            continue
        return config 

    return None
