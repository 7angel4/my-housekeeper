import sqlite3
from constants import *

class Database(object):
    """Singleton database"""
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def create_tables(self):
        for table_name, columns in DB_COLUMNS.items():
            command = f"CREATE TABLE IF NOT EXISTS {table_name} ("
            for column, requirement in columns.items():
                command += f"{column} {requirement},"
                
            command += f'PRIMARY KEY ({parse_pk(table_name)}))'
            self.cursor.execute(command)
        
        self.connection.commit()

    def __init__(self):
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_query(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
