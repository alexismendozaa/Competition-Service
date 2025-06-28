from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes import competition_routes
from flask_cors import CORS

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
            "/compe/select/{competition_id}": {
                "get": {
                    "summary": "Obtiene la información de una competencia específica",
                    "description": "Recibe un ID de competencia y devuelve la información de esa competencia.",
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
                            "description": "Detalles de la competencia",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "competition_id": {
                                        "type": "string",
                                        "example": "318e31b0-a9f1-4203-ae5f-f593c032ec62"
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "La competencia comenzó el 2025-06-21 13:37:47."
                                    },
                                    "participants": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "email": {
                                                    "type": "string",
                                                    "example": "afmendozaf@uce.edu.ec"
                                                },
                                                "name": {
                                                    "type": "string",
                                                    "example": "Alexis Mendoza"
                                                },
                                                "posts": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "created_at": {
                                                                "type": "string",
                                                                "example": "2025-06-21 18:23:29"
                                                            },
                                                            "description": {
                                                                "type": "string",
                                                                "example": "un gatooo"
                                                            },
                                                            "image_url": {
                                                                "type": "string",
                                                                "example": "https://buket-avatars.s3.us-east-1.amazonaws.com/gato3.jpg"
                                                            },
                                                            "likes": {
                                                                "type": "integer",
                                                                "example": 1
                                                            },
                                                            "post_id": {
                                                                "type": "string",
                                                                "example": "210d58f3-bb3f-4af7-9381-5e5c6ec61353"
                                                            }
                                                        }
                                                    }
                                                },
                                                "posts_count": {
                                                    "type": "integer",
                                                    "example": 1
                                                }
                                            }
                                        }
                                    },
                                    "winners": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "email": {
                                                    "type": "string",
                                                    "example": "afmendozaf@uce.edu.ec"
                                                },
                                                "total_likes": {
                                                    "type": "integer",
                                                    "example": 1
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Competencia no encontrada",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "Competencia no encontrada"
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
    SWAGGER_URL = '/api-docs-compe-select'
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
