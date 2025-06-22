import sqlite3

connect = sqlite3.connect("users.db")
cursor = connect.cursor()

cursor.execute("""
   CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name VARCHAR(100) NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        user_id INTEGER NOT NULL        
   ) 
    
""")
connect.commit()

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, full_name, username, user_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO users (full_name, username, user_id) VALUES (?, ?, ?)', (full_name, username, user_id))

    def exist_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT user_id from 'users' WHERE user_id=?", (user_id,)).fetchmany(1)
            return bool(len(result))


