from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from app.routes import competition_routes

def create_app():
    app = Flask(__name__)

    # Configurar CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Definir el esquema de Swagger
    swagger_spec = {
        "swagger": "2.0",
        "info": {
            "title": "Competition Service",
            "version": "1.0.0",
            "description": "API para gestionar competencias y recibir actualizaciones en tiempo real."
        },
        "paths": {
            "/compe/history": {
                "get": {
                    "summary": "Obtiene los ganadores históricos de todas las competencias",
                    "description": "Recibe todas las competencias y muestra a sus ganadores históricos.",
                    "responses": {
                        "200": {
                            "description": "Ganadores históricos de todas las competencias",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "status": {
                                        "type": "string",
                                        "example": "success"
                                    },
                                    "historical_winners": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "competition_id": {
                                                    "type": "string",
                                                    "example": "318e31b0-a9f1-4203-ae5f-f593c032ec62"
                                                },
                                                "competition_date": {
                                                    "type": "string",
                                                    "example": "2025-06-21"
                                                },
                                                "username": {
                                                    "type": "string",
                                                    "example": "Alexis Mendoza"
                                                },
                                                "email": {
                                                    "type": "string",
                                                    "example": "afmendozaf@uce.edu.ec"
                                                },
                                                "post": {
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
                        "404": {
                            "description": "No se encontraron ganadores históricos",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "status": {
                                        "type": "string",
                                        "example": "no-data"
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "No se encontraron ganadores históricos."
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
    SWAGGER_URL = '/api-docs-compe-history'
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
