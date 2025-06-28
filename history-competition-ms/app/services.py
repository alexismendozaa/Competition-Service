import redis
from app.config import Config
import json
from datetime import datetime

def get_historical_winners():
    redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True)

    historical_winners = []

    # Obtener todas las competencias
    competition_keys = redis_client.keys('competition:*:finalized')  # Filtrar solo las competencias finalizadas

    for competition_key in competition_keys:
        competition_id = competition_key.split(":")[1]  # Obtener el ID de la competencia
        competition_data = redis_client.get(f'competition:{competition_id}:data')

        if competition_data:
            competition_data = json.loads(competition_data)
            competition_date = redis_client.get(f'competition:{competition_id}:start_date')

            # Ordenar los usuarios por el total de likes, de mayor a menor
            sorted_users = sorted(competition_data.items(), key=lambda x: x[1]['total_likes'], reverse=True)
            top_users = [user for user in sorted_users if user[1]['total_likes'] == sorted_users[0][1]['total_likes']]

            for user in top_users:
                winner_info = {
                    "competition_id": competition_id,
                    "competition_date": competition_date,
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
                historical_winners.append(winner_info)

    return historical_winners
