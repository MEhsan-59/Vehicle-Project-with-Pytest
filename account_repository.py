# account_repository.py
import sqlite3
import json
import os
from datetime import datetime
from account_model import Model
from db_connection import DatabaseConnection
from config import Config
import security

class AccountRepository:
    def __init__(self):
        self.db = DatabaseConnection("Bank.db")
        self.create_table()
        self.active_account_file = "active_account.json" 

    def create_table(self):
        with self.db.get_session() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON") 
            cursor.execute("""CREATE TABLE IF NOT EXISTS Bank(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_id TEXT,
                Password TEXT,
                Created_at TEXT,
                Balance INTEGER DEFAULT 0
            )""")

    def save_account(self, user_id, password):
        with self.db.get_session() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Bank (User_id, Password, Created_at, Balance) VALUES (?,?,?,?)", 
                           (user_id, password, datetime.now().strftime("%d.%m.%Y %H:%M:%S"), Config.DEFAULT_BALANCE))

    def _save_active_account_to_json(self, user_id, password):
        data = {"user_id": user_id, "password": password}
        with open(self.active_account_file, "w") as f:
            json.dump(data, f)

    def _load_active_account_from_json(self):
        if not os.path.exists(self.active_account_file):
            return None, None
        try:
            with open(self.active_account_file, "r") as f:
                data = json.load(f)
            return data.get("user_id"), data.get("password")
        except (json.JSONDecodeError, IOError):
            return None, None

    def insert_active_account(self, user_id, password):
        self._save_active_account_to_json(user_id, password)

    def load_active_account(self):
        user_id, password = self._load_active_account_from_json()
        if user_id:
            return self.check_account(user_id)
        return None

    def update_balance(self, user_id, balance):
        with self.db.get_session() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Bank SET Balance = Balance + ? WHERE LOWER(User_id) = LOWER(?)", (balance, user_id))
            if cursor.rowcount == 0:
                print(f"WARNING: No user found with id {user_id}")

    def check_account(self, user_id, password=None):
        with self.db.get_session() as conn:
            cursor = conn.cursor()
            if not password:
                cursor.execute("SELECT * FROM Bank WHERE User_id=?", (user_id, ))
            else:
                cursor.execute("SELECT * FROM Bank WHERE User_id=? AND Password=?", (user_id, password))
            raw_row = cursor.fetchall()
            if raw_row:
                raw_row = raw_row[0]
                clear_row = Model(*raw_row)
                print(f"DEBUG: Loaded balance for {user_id}: {clear_row.balance}") 
                return clear_row
            return None