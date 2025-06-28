import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_COMMENTS = os.getenv("DB_COMMENTS")
    DB_USERS = os.getenv("DB_USERS")
    DB_POST = os.getenv("DB_POST")
    DB_LIKES = os.getenv("DB_LIKES")
    DB_SSL = os.getenv("DB_SSL") == 'true'
    JWT_SECRET = os.getenv("JWT_SECRET")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    PORT = int(os.getenv("PORT", 3023))
