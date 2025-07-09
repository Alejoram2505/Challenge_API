from flask import Blueprint, request, jsonify
from app.services.config_service import save_mock_config, get_all_mock_configs, delete_mock_config

configure_mock_bp = Blueprint("configure_mock", __name__)

@configure_mock_bp.route("/configure-mock", methods=["POST"])
def configure_mock():
    """
    Crear un nuevo mock
    ---
    tags:
      - Mock Config
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              path:
                type: string
              method:
                type: string
              query_params:
                type: object
              body_params:
                type: object
              headers:
                type: object
              response_status:
                type: integer
              response_body:
                type: object
              content_type:
                type: string
              delay_ms:
                type: integer
            example:
              path: "/api/mock"
              method: "GET"
              query_params: {}
              body_params: {}
              headers: {}
              response_status: 200
              response_body: {"message": "Hello"}
              content_type: "application/json"
              delay_ms: 0
    responses:
      201:
        description: Mock creado exitosamente
      400:
        description: Error al crear mock
    """
    data = request.get_json()
    success, result = save_mock_config(data)

    if not success:
        return jsonify({"error": result}), 400

    return jsonify({"message": "Configuración registrada", "id": result}), 201


@configure_mock_bp.route("/configure-mock", methods=["GET"])
def list_mocks():
    """
    Obtener todos los mocks registrados
    ---
    tags:
      - Mock Config
    responses:
      200:
        description: Lista de mocks
    """
    configs = get_all_mock_configs()
    return jsonify(configs), 200


@configure_mock_bp.route("/configure-mock/<int:config_id>", methods=["DELETE"])
def delete_mock(config_id):
    """
    Eliminar un mock por ID
    ---
    tags:
      - Mock Config
    parameters:
      - name: config_id
        in: path
        type: integer
        required: true
        description: ID del mock a eliminar
    responses:
      200:
        description: Mock eliminado correctamente
      404:
        description: Mock no encontrado
    """
    success, message = delete_mock_config(config_id)

    if not success:
        return jsonify({"error": message}), 404

    return jsonify({"message": message}), 200
