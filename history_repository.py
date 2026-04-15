#history_repository.py
from db_connection import DatabaseConnection
from models import HistoryEntry
import datetime

class HistoryRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db
        self._create_table()

    def _create_table(self):
        with self.db.get_session() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS history(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id INTEGER NOT NULL,
                    car_no TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    part_name TEXT,
                    changed_km INTEGER,
                    changed_date TEXT,
                    action_timestamp TEXT NOT NULL,
                    active_user TEXT NOT NULL,
                    details TEXT,
                    FOREIGN KEY(vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_history_vehicle_id ON history(vehicle_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_history_car_no ON history(car_no)")

    def add_entry(self, entry: HistoryEntry):
        with self.db.get_session() as conn:
            conn.execute("""
                INSERT INTO history
                (vehicle_id, car_no, action_type, part_name, changed_km, changed_date,
                 action_timestamp, active_user, details)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (entry.vehicle_id, entry.car_no, entry.action_type, entry.part_name,
                  entry.changed_km, entry.changed_date, entry.action_timestamp,
                  entry.active_user, entry.details))

    def get_all(self, active_user: str) -> list[HistoryEntry]:
        with self.db.get_session() as conn:
            rows = conn.execute("""
                SELECT id, vehicle_id, car_no, action_type, part_name,
                       changed_km, changed_date, action_timestamp, active_user, details
                FROM history
                WHERE active_user=?
                ORDER BY action_timestamp DESC
            """, (active_user,)).fetchall()
            return [HistoryEntry(*row) for row in rows]

    def get_by_car(self, car_no: str, active_user: str) -> list[HistoryEntry]:
        with self.db.get_session() as conn:
            rows = conn.execute("""
                SELECT id, vehicle_id, car_no, action_type, part_name,
                       changed_km, changed_date, action_timestamp, active_user, details
                FROM history
                WHERE active_user=? AND car_no=?
                ORDER BY action_timestamp DESC
            """, (active_user, car_no)).fetchall()
            return [HistoryEntry(*row) for row in rows]

    def get_by_part(self, part_name: str, active_user: str) -> list[HistoryEntry]:
        with self.db.get_session() as conn:
            rows = conn.execute("""
                SELECT id, vehicle_id, car_no, action_type, part_name,
                       changed_km, changed_date, action_timestamp, active_user, details
                FROM history
                WHERE active_user=? AND part_name=?
                ORDER BY action_timestamp DESC
            """, (active_user, part_name)).fetchall()
            return [HistoryEntry(*row) for row in rows]