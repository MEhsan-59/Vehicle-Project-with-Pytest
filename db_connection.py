#db_connection.py
import sqlite3
from contextlib import contextmanager

class DatabaseConnection:
    def __init__(self, db_name="Vehicle_app.db"):  
        self.db_name = db_name

    @contextmanager
    def get_session(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except sqlite3.Error:
            conn.rollback()
            raise
        finally:
            conn.close()