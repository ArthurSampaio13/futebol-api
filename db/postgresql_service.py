import psycopg2
from .database_service import DatabaseService
from config.settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

class PostgreSQLService(DatabaseService):
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

    def insert_data(self, query, data):
        with self.conn.cursor() as cursor:
            cursor.executemany(query, data)
        self.conn.commit()

    def close(self):
        self.conn.close()