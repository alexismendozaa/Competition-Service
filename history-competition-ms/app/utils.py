import psycopg2
from app.config import Config

def get_db_connection(db_type):
    """
    Devuelve una conexión a la base de datos especificada según el tipo de tabla.
    
    db_type: El nombre de la base de datos (e.g. 'users', 'post', 'reactions').
    """
    db_name = {
        'users': Config.DB_USERS,
        'post': Config.DB_POST,
        'reactions': Config.DB_LIKES,
        'comments': Config.DB_COMMENTS
    }.get(db_type)
    
    if not db_name:
        raise ValueError(f"Base de datos desconocida: {db_type}")

    try:
        # Realizamos la conexión a la base de datos correcta
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=db_name,
            sslmode='require' if Config.DB_SSL else 'disable'
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos {db_name}: {e}")
        return None
