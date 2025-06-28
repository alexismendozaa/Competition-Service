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
            "title": "Competition Service",
            "version": "1.0.0",
            "description": "API para gestionar competencias y recibir actualizaciones en tiempo real."
        },
        "paths": {
            "/compe/win/{competition_id}": {
                "get": {
                    "summary": "Obtiene el o los ganadores de una competencia",
                    "description": "Recibe un ID de competencia y devuelve el o los ganadores con sus detalles.",
                    "parameters": [
                        {
                            "name": "competition_id",
                            "in": "path",
                            "required": True,
                            "type": "string",
                            "description": "ID de la competencia"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Ganadores de la competencia",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "status": {
                                        "type": "string",
                                        "example": "finished"
                                    },
                                    "winners": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "username": {
                                                    "type": "string",
                                                    "example": "Alexis Mendoza"
                                                },
                                                "email": {
                                                    "type": "string",
                                                    "example": "afmendozaf@uce.edu.ec"
                                                },
                                                "post": {
                                                    "type": "string",
                                                    "example": "un gatooo"
                                                },
                                                "total_likes": {
                                                    "type": "integer",
                                                    "example": 10
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Competencia en progreso",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "status": {
                                        "type": "string",
                                        "example": "in-progress"
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "La competencia está en progreso."
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # Configuración de Swagger UI
    SWAGGER_URL = '/api-docs-compe-win'
    API_URL = '/swagger-spec'
    swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Competition Service"})
    app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

    # Crear una ruta para servir la especificación de Swagger
    @app.route('/swagger-spec')
    def swagger_spec_route():
        return jsonify(swagger_spec)

    # Registrar las rutas adicionales
    app.register_blueprint(competition_routes)

    return app
