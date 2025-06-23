import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

connect = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = connect.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users
    (
        id serial PRIMARY KEY NOT NULL,
        full_name VARCHAR(100) NOT NULL, 
        username VARCHAR(50) NOT NULL,
        user_id BIGINT NOT NULL
    )
''')


class Database:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host,
                                           port=db_port)
        self.cursor = self.connection.cursor()

    def add_user(self, full_name, username, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (full_name, username, user_id) VALUES (%s, %s, %s)",
                                       (full_name, username, user_id))

    def exist_user(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT user_id FROM users WHERE user_id=%s", (user_id,))
            return self.cursor.fetchone()


connect.commit()
connect.close()
