import redis
from app.config import Config
import json

def get_winner(competition_id):
    redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True)

    # Verificar si la competencia ha sido finalizada
    competition_finalized = redis_client.get(f'competition:{competition_id}:finalized')

    if competition_finalized:
        # Obtener los datos de la competencia desde Redis
        competition_data = redis_client.get(f'competition:{competition_id}:data')
        if not competition_data:
            return None, "Datos de la competencia no encontrados."

        competition_data = json.loads(competition_data)

        # Ordenar a los usuarios por el total de likes, de mayor a menor
        sorted_users = sorted(competition_data.items(), key=lambda x: x[1]['total_likes'], reverse=True)

        # Obtener el o los ganadores (en caso de empate por likes)
        top_users = [user for user in sorted_users if user[1]['total_likes'] == sorted_users[0][1]['total_likes']]

        winners = []
        for user in top_users:
            winner_info = {
                "username": user[1]['username'],
                "email": user[1]['email'],
                "post": {
                    "created_at": user[1]['posts'][0]['created_at'] if user[1]['posts'] else "No posts",
                    "description": user[1]['posts'][0]['description'] if user[1]['posts'] else "No description",
                    "image_url": user[1]['posts'][0]['image_url'] if user[1]['posts'] else "No image",
                    "likes": user[1]['posts'][0]['likes'] if user[1]['posts'] else 0,
                    "post_id": user[1]['posts'][0]['post_id'] if user[1]['posts'] else "No post id"
                },
                "total_likes": user[1]['total_likes']
            }
            winners.append(winner_info)

        return winners, None
    else:
        return None, "La competencia está en progreso."
