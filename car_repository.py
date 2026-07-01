#car_repository.py
from db_connection import DatabaseConnection
from models import Vehicle
import sqlite3

class CarRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db
        self._create_table()

    def _create_table(self):
        with self.db.get_session() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vehicles(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    car_no TEXT UNIQUE NOT NULL,
                    model TEXT NOT NULL,
                    company TEXT NOT NULL,
                    onground_km INTEGER NOT NULL,
                    active_user TEXT NOT NULL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_vehicles_car_no ON vehicles(car_no)")

    def insert(self, vehicle: Vehicle) -> int:
        with self.db.get_session() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO vehicles (car_no, model, company, onground_km, active_user)
                VALUES (?,?,?,?,?)
            """, (vehicle.car_no, vehicle.model, vehicle.company,
                vehicle.onground_km, vehicle.active_user))
            return cur.lastrowid

    def load_all(self, active_user) -> list[Vehicle]:
        with self.db.get_session() as conn:
            rows = conn.execute(
                "SELECT id, car_no, model, company, onground_km, active_user FROM vehicles WHERE active_user=?",
            (active_user, )).fetchall()
            return [Vehicle(*row) for row in rows]

    def get_by_car_no(self, car_no: str, active_user: str) -> Vehicle | None:
        with self.db.get_session() as conn:
            row = conn.execute("""
                SELECT id, car_no, model, company, onground_km, active_user
                FROM vehicles WHERE car_no=? AND active_user=?
            """, (car_no, active_user)).fetchone()
            return Vehicle(*row) if row else None

    def update_km(self, vehicle: Vehicle):
        with self.db.get_session() as conn:
            conn.execute(
                "UPDATE vehicles SET onground_km=? WHERE id=?",
                (vehicle.onground_km, vehicle.id)
            )

    def delete(self, vehicle: Vehicle):
        with self.db.get_session() as conn:
            conn.execute("DELETE FROM vehicles WHERE id=?", (vehicle.id,))
    
    def get_ongkm_by_car_id(self, car_id, active_user) -> int | None:
        with self.db.get_session() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT onground_km FROM vehicles WHERE id=? and active_user=?", (car_id, active_user))
            row = cursor.fetchone()
            return row[0] if row else None