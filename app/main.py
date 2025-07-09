from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import os

# Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar extensiones
    Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Mock API Config",
            "description": "API para crear, listar y eliminar mocks personalizados",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http"]
    })
    db.init_app(app)

    # Rutas internas
    @app.route("/ping")
    def ping():
        """
        Ping de prueba
        ---
        responses:
          200:
            description: OK
        """
        return {"message": "pong"}, 200

    # Servir interfaz web
    @app.route("/")
    def frontend():
        return render_template("index.html")

    # Registrar blueprints
    from app.routes.configure_mock import configure_mock_bp
    app.register_blueprint(configure_mock_bp)

    from app.routes.mock_executor import mock_executor_bp
    app.register_blueprint(mock_executor_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
