import redis
from app.config import Config
from app.utils import get_db_connection
import uuid
import json
from datetime import datetime, timedelta

def end_competition(competition_id):
    try:
        # Conexión a Redis
        redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True)

        # Buscar la competencia en Redis
        competition_data = redis_client.get(f'competition:{competition_id}:data')

        if competition_data:
            # Convertir los datos a JSON
            competition_data = json.loads(competition_data)

            # Congelar los datos de la competencia (guardar en una nueva clave)
            redis_client.set(f'competition:{competition_id}:finalized', json.dumps(competition_data))

            # Marcar que la competencia ha finalizado
            redis_client.set(f'competition:{competition_id}:status', 'finalizado')  # Establece el estado 'finalizado' en Redis

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

            # Devolver las estadísticas y el número de participantes
            return {
                "message": "Competencia finalizada",
                "total_participants": total_participants,
                "statistics": statistics
            }
        else:
            return {"message": "Competencia no encontrada"}, 404

    except Exception as e:
        return {"message": f"Error al finalizar la competencia: {str(e)}"}, 500

def update_competition_data(competition_id, new_data):
    try:
        # Conexión a Redis
        redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True)

        # Verificar si la competencia está finalizada
        competition_status = redis_client.get(f'competition:{competition_id}:status')

        if competition_status == 'finalizado':
            return {"message": "La competencia ha finalizado, no se pueden realizar más actualizaciones."}, 400

        # Lógica para actualizar los datos si la competencia no ha finalizado
        redis_client.set(f'competition:{competition_id}:data', json.dumps(new_data))
        return {"message": "Datos actualizados con éxito."}

    except Exception as e:
        return {"message": f"Error al actualizar los datos: {str(e)}"}, 500
