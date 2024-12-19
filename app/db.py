import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Чтение конфигурации из переменных окружения
DATABASE_CONFIG = {
    "dbname": os.getenv("DB_NAME", "default_db"),
    "user": os.getenv("DB_USER", "default_user"),
    "password": os.getenv("DB_PASSWORD", "default_password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),  # Преобразуем порт в число
}

def get_db_connection():
    """Создает подключение к PostgreSQL."""
    conn = psycopg2.connect(**DATABASE_CONFIG, cursor_factory=RealDictCursor)
    return conn
