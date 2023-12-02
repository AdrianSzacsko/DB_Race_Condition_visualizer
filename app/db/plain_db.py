import psycopg2
from app.settings import settings
from threading import Thread


# Database connection setup
def db_connection():
    try:
        conn = psycopg2.connect(
            database=settings.DB_NAME,
            user=settings.DB_USERNAME,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT
        )
        return conn
    except psycopg2.Error as error:
        print("Error while connecting to PostgreSQL:", error)
    return None