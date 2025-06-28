from flask import Blueprint, jsonify, request
import redis
from app.config import Config
import json

competition_routes = Blueprint('competition_routes', __name__)

# Ruta para manejar el GET en /compe/select con un competition_id
@competition_routes.route('/compe/select/<competition_id>', methods=['GET'])
def select_competition_endpoint(competition_id):
    redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True)
    
    # Buscar la competencia en Redis con la clave correcta
    competition_data = redis_client.get(f'competition:{competition_id}:data')

    # Verificar si la competencia existe en Redis
    if competition_data:
        # Si la competencia existe, convertir los datos
        competition_data = json.loads(competition_data)
        
        # Verificar si la competencia ha sido finalizada
        competition_finalized = redis_client.get(f'competition:{competition_id}:finalized')

        if competition_finalized:
            competition_status = "finished"
        else:
            # Verificar el estado de la competencia en Redis
            competition_status = redis_client.get(f'competition:{competition_id}:status')
            
            # Si no se encuentra el estado, consideramos que la competencia está activa
            if competition_status is None:
                competition_status = "active"
        
        # Ordenar los usuarios por el total de likes, de mayor a menor
        sorted_users = sorted(competition_data.items(), key=lambda x: x[1]['total_likes'], reverse=True)
        
        # Obtener los 3 primeros usuarios (Top 3)
        top_3 = sorted_users[:3]
        
        # Crear una respuesta con los datos de la competencia y los top 3
        response = {
            "competition_data": competition_data,  # Datos completos de la competencia
            "status": competition_status,  # Estado de la competencia
            "top_3": [
                {
                    "username": user[1]['username'],
                    "email": user[1]['email'],
                    "total_likes": user[1]['total_likes']
                } 
                for user in top_3
            ]
        }
        
        return jsonify(response)
    else:
        # Si no se encuentra la competencia, se asume que ha finalizado
        return jsonify({"message": "La competencia ha finalizado."}), 404
