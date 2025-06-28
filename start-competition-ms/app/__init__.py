from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes import competition_routes

def create_app():
    app = Flask(__name__)

    # Configurar CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Definir el esquema de Swagger directamente en el código
    swagger_spec = {
        "swagger": "2.0",
        "info": {
            "title": "Start Competition Service",
            "version": "1.0.0",
            "description": "API para iniciar una competencia diaria de posts con más likes."
        },
        "paths": {
            "/compe/start": {
                "post": {
                    "summary": "Inicia una nueva competencia de posts.",
                    "responses": {
                        "200": {
                            "description": "Competencia iniciada correctamente.",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # Configuración de Swagger UI (sin necesidad de un archivo .json externo)
    SWAGGER_URL = '/api-docs-compe-start'
    API_URL = '/swagger-spec'  # Usaremos esta ruta para servir el esquema de Swagger
    swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Start Competition Service"})
    app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

    # Crear una ruta para servir la especificación de Swagger (sin archivo .json)
    @app.route('/swagger-spec')
    def swagger_spec_route():
        return jsonify(swagger_spec)

    # Registrar las rutas adicionales
    app.register_blueprint(competition_routes)

    return app
