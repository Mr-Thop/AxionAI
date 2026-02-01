import os
from dotenv import load_dotenv
import psycopg2
import mysql.connector as sql

load_dotenv()

class DB:
    def __init__(self):
        self.string = os.getenv("Connection_String")
        self.collection = os.getenv("Collection_Name")
        self.host = os.getenv("Host")
        self.port = os.getenv("Port")
        self.user = os.getenv("User")
        self.password = os.getenv("Password")
        self.db = os.getenv("DB_Name")
    
    def connect_PS(self):
        self.connection_PS = psycopg2.connect(self.string)
        self.cursor_PS = self.connection_PS.cursor()
    
    def connect_MS(self):
        self.connection_MS = sql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            database = self.db
        )
        self.cursor_MS = self.connection_MS.cursor()

    def insert(self, data):
        insert_query = f"INSERT INTO users(name,email,date,time,password) VALUES %s"
        self.cursor_MS.execute(insert_query, (data,))


    def clear(self):
        self.cursor_PS.execute(f"DELETE FROM {self.collection}")
        self.connection_PS.commit()
    
    def close_PS(self):
        self.cursor_PS.close()
        self.connection_PS.close()
    
    def close_MS(self):
        self.cursor_MS.close()
        self.connection_MS.close()


