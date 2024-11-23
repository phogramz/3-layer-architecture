import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_CONFIG = {
    "dbname": "3lrar_db",
    "user": "usermaxim",
    "password": "110622",
    "host": "localhost",
    "port": 5432,
}

def get_db_connection():
    """Создает подключение к PostgreSQL."""
    conn = psycopg2.connect(**DATABASE_CONFIG, cursor_factory=RealDictCursor)
    return conn