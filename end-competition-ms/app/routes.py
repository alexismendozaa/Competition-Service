from flask import Blueprint, jsonify, request
import redis
from app.config import Config
import json
from datetime import datetime


competition_routes = Blueprint('competition_routes', __name__)



@competition_routes.route('/compe/end/<competition_id>', methods=['POST'])
def end_competition(competition_id):
    redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True)
    
    # Buscar la competencia en Redis con la clave correcta
    competition_data = redis_client.get(f'competition:{competition_id}:data')
    
    if competition_data:
        # Si la competencia existe, convertir los datos
        competition_data = json.loads(competition_data)
        
        # Congelar los datos de la competencia (no se permitirán más cambios)
        redis_client.set(f'competition:{competition_id}:finalized', json.dumps(competition_data))
        
        # Generar estadísticas de la competencia
        total_participants = len(competition_data)
        statistics = []
        
        for user, data in competition_data.items():
            stats = {
                "username": data["username"],
                "email": data["email"],
                "total_posts": len(data["posts"]),
                "total_likes": data["total_likes"]
            }
            statistics.append(stats)
        
        # Ordenar las estadísticas por likes, de mayor a menor
        statistics.sort(key=lambda x: x["total_likes"], reverse=True)
        
        # Respuesta con estadísticas
        response = {
            "message": "Competencia finalizada",
            "total_participants": total_participants,
            "statistics": statistics
        }
        
        return jsonify(response)
    
    else:
        return jsonify({"message": "Competencia no encontrada"}), 404
