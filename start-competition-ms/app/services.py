import redis
from app.config import Config
from app.utils import get_db_connection
import uuid
import json
from datetime import datetime, timedelta

def start_competition():
    try:
        # Conexión a Redis (para cache temporal de likes)
        redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True)
        
        # Conexión a las bases de datos: users, post, reactions
        conn_users = get_db_connection('users')  # Conexión a la base de datos users
        conn_posts = get_db_connection('post')  # Conexión a la base de datos post
        conn_reactions = get_db_connection('reactions')  # Conexión a la base de datos reactions

        if conn_users and conn_posts and conn_reactions:
            # Lógica de la competencia
            competition_id = str(uuid.uuid4())  # ID único para la competencia
            
            # Verificar si la competencia ya está en progreso
            competition_status = redis_client.get(f'competition:{competition_id}:status')
            if competition_status == 'in-progress':
                return {"message": "La competencia ya está en progreso."}

            # Establecer el estado de la competencia como "in-progress"
            redis_client.set(f'competition:{competition_id}:status', 'in-progress', ex=86400)  # Competencia de 24 horas

            # Obtener la fecha y hora actual
            current_time = datetime.now()
            start_time = current_time - timedelta(days=1)  # 24 horas antes

            # Convertir `current_time` a cadena
            current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

            # 1. Obtener todos los usuarios
            cursor = conn_users.cursor()
            cursor.execute('SELECT id, username, email FROM "Users"')
            users = cursor.fetchall()

            # 2. Obtener los posts de los usuarios en las últimas 24 horas
            competition_data = {}  # Diccionario para almacenar los datos de la competencia
            user_likes = {}  # Diccionario para almacenar los likes de los usuarios

            for user in users:
                user_id, username, email = user
                cursor = conn_posts.cursor()  # Conexión a la base de datos de posts
                cursor.execute('''  
                    SELECT id, created_at, image_url, description FROM post 
                    WHERE user_id = %s AND created_at > %s
                ''', (user_id, start_time))  # Obtener los posts de las últimas 24 horas
                posts = cursor.fetchall()  # Obtener los posts de este usuario
                user_posts = []  # Lista para almacenar los posts de este usuario con sus likes
                total_likes = 0  # Acumulador de likes de este usuario

                for post in posts:
                    post_id, created_at, image_url, description = post
                    cursor = conn_reactions.cursor()  # Conexión a la base de datos de reactions
                    cursor.execute('SELECT COUNT(*) FROM reactions WHERE post_id = %s', (post_id,))
                    likes_count = cursor.fetchone()[0]  # Contamos los likes de ese post
                    total_likes += likes_count  # Sumar los likes de este post
                    
                    # Convertir `created_at` a cadena
                    created_at_str = created_at.strftime('%Y-%m-%d %H:%M:%S')

                    user_posts.append({
                        "post_id": post_id,
                        "image_url": image_url,
                        "created_at": created_at_str,
                        "description": description,
                        "likes": likes_count
                    })

                # Guardamos los posts y likes en el diccionario de competencia
                competition_data[email] = {
                    "username": username,
                    "email": email,
                    "posts": user_posts,
                    "total_likes": total_likes  # Número total de likes en las últimas 24 horas
                }

                # Guardamos los likes totales para comparar más tarde
                user_likes[email] = total_likes

            # 3. Guardar la información de la competencia (en Redis o en la base de datos)
            redis_client.set(f"competition:{competition_id}:data", json.dumps(competition_data))

            # 4. Determinar al ganador basado en los likes
            winner = None
            max_likes = 0
            for user_email, total_likes in user_likes.items():
                if total_likes > max_likes:
                    max_likes = total_likes
                    winner = user_email

            # Guardar el ganador en Redis
            winners = [{
                "email": winner,
                "total_likes": max_likes
            }] if winner else []

            redis_client.set(f"competition:{competition_id}:winners", json.dumps(winners))

            # Devolver respuesta con los participantes y sus posts/likes
            participants_info = []
            for user_email, user_data in competition_data.items():
                user_info = {
                    "name": user_data["username"],
                    "email": user_email,
                    "posts_count": len(user_data["posts"]),
                    "posts": []
                }
                for post in user_data["posts"]:
                    user_info["posts"].append({
                        "post_id": post["post_id"],
                        "image_url": post["image_url"],
                        "created_at": post["created_at"],
                        "description": post["description"],
                        "likes": post["likes"]
                    })
                participants_info.append(user_info)

            # Cerrar las conexiones a las bases de datos
            conn_users.close()
            conn_posts.close()
            conn_reactions.close()

            return {
                "message": f"La competencia comenzó el {current_time_str}.",
                "competition_id": competition_id,
                "participants": participants_info,
                "winners": winners
            }
        else:
            return {"message": "Error al conectar con las bases de datos."}
    except Exception as e:
        return {"message": f"Error al iniciar la competencia: {str(e)}"}
