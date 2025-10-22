import pymysql
import os

# Configuración de conexión
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root123"),
    "database": os.getenv("DB_NAME", "babycare"),
    "cursorclass": pymysql.cursors.DictCursor
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)
