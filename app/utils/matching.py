import re
from app.models.mock_config import MockConfig

def match_value(expected, actual):
    if expected is None:
        return True  # Hace que no se requiera un campo
    if actual is None:
        return False

    if isinstance(expected, str):
        if expected.startswith("regex:"):
            return re.fullmatch(expected[6:], actual or "") is not None
        elif expected.startswith("startsWith:"):
            return (actual or "").startswith(expected[11:])
        elif expected.startswith("ignorecase:"):
            return expected[11:].lower() == (actual or "").lower()

    return expected == actual

def match_dict(expected_dict, actual_dict):
    for key, expected_val in expected_dict.items():
        actual_val = actual_dict.get(key)
        if not match_value(expected_val, actual_val):
            return False
    return True

def find_matching_mock(path, method, query_params, body_params, headers):
    candidates = MockConfig.query.filter_by(path=path, method=method.upper()).all()

    for mock in candidates:
        if mock.query_params and not match_dict(mock.query_params, query_params):
            continue
        if mock.body_params and not match_dict(mock.body_params, body_params):
            continue
        if mock.headers and not match_dict(mock.headers, headers):
            continue
        return mock

    return None
