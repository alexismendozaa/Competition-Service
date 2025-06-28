from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes import competition_routes  # Importamos las rutas
from app.services import end_competition  # Importamos la función end_competition para finalizar la competencia

def create_app():
    app = Flask(__name__)

    # Configurar CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Configuración de Swagger UI
    SWAGGER_URL = '/api-docs-compe-end'  # Ruta actualizada para Swagger de la nueva ruta
    API_URL = '/swagger-spec'
    swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Competition Service"})
    app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

    # Crear una ruta para servir la especificación de Swagger
    @app.route('/swagger-spec')
    def swagger_spec_route():
        return jsonify({
            "swagger": "2.0",
            "info": {
                "title": "Competition Service",
                "version": "1.0.0",
                "description": "API para gestionar competencias y recibir actualizaciones en tiempo real."
            },
            "paths": {
                "/compe/end/{competition_id}": {
                    "post": {
                        "summary": "Finaliza la competencia y congela los datos",
                        "parameters": [
                            {
                                "name": "competition_id",
                                "in": "path",
                                "required": True,
                                "type": "string",
                                "description": "ID de la competencia a finalizar"
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Competencia finalizada",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {"type": "string", "example": "Competencia finalizada"},
                                        "total_participants": {"type": "integer", "example": 5},
                                        "statistics": {"type": "array", "items": {"type": "object"}}}
                            },
                            "404": {
                                "description": "Competencia no encontrada"
                            }
                        }
                    }
                }
            }
      }  })

    # Registrar las rutas adicionales
    app.register_blueprint(competition_routes)

    # Ruta para finalizar la competencia
    @app.route('/compe/end/<competition_id>', methods=['POST'])
    def end_competition_route(competition_id):
        result = end_competition(competition_id)  # Llamamos a la función para finalizar la competencia
        return jsonify(result)

    return app
