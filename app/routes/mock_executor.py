from flask import Blueprint, request, jsonify, make_response
from app.utils.matching import find_matching_mock
import time

mock_executor_bp = Blueprint("mock_executor", __name__)

@mock_executor_bp.route("/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def handle_any_mock(subpath):
    path = f"/{subpath}"
    method = request.method

    # Extraer datos del request
    query_params = request.args.to_dict()
    body_params = {}
    if request.is_json:
        body_params = request.get_json()
    headers = dict(request.headers)

    # Buscar un mock que coincida
    mock = find_matching_mock(path, method, query_params, body_params, headers)
    if not mock:
        return jsonify({"error": "No matching mock configuration found"}), 404

    # Simular latencia si existe
    if mock.delay_ms:
        time.sleep(mock.delay_ms / 1000.0)

    response = make_response(jsonify(mock.response_body), mock.response_status)
    response.headers["Content-Type"] = mock.content_type
    return response
