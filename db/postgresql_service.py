import psycopg2
from .database_service import DatabaseService
from config.settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import os

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class PostgreSQLService(DatabaseService):
    def __init__(self):
        self.conn = psycopg2.connect(DB_URL)
        
    def insert_data(self, query, data):
        with self.conn.cursor() as cursor:
            cursor.executemany(query, data)
        self.conn.commit()

    def close(self):
        self.conn.close()