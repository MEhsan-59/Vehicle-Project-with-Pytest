#maintenance_repository.py
from db_connection import DatabaseConnection
from models import MaintenanceRecord, VehicleMaintenanceDetail

class MaintenanceRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db
        self._create_table()

    def _create_table(self):
        with self.db.get_session() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS maintenance(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id INTEGER NOT NULL,
                    part_id INTEGER NOT NULL,
                    changed_km INTEGER NOT NULL,
                    next_changed_km INTEGER NOT NULL,
                    changed_date TEXT NOT NULL,
                    next_changed_date TEXT NOT NULL,
                    UNIQUE(vehicle_id, part_id),
                    FOREIGN KEY(vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
                    FOREIGN KEY(part_id) REFERENCES config(id) ON DELETE CASCADE
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_maintenance_vehicle_id ON maintenance(vehicle_id)")

    def get_record(self, vehicle_id: int, part_id: int) -> MaintenanceRecord | None:
        with self.db.get_session() as conn:
            row = conn.execute("""
                SELECT id, vehicle_id, part_id, changed_km, next_changed_km,
                       changed_date, next_changed_date
                FROM maintenance WHERE vehicle_id=? AND part_id=?
            """, (vehicle_id, part_id)).fetchone()
            return MaintenanceRecord(*row) if row else None

    def upsert(self, maintenance: MaintenanceRecord):
        with self.db.get_session() as conn:
            conn.execute("""
                INSERT INTO maintenance
                (vehicle_id, part_id, changed_km, next_changed_km, changed_date, next_changed_date)
                VALUES (?,?,?,?,?,?)
                ON CONFLICT(vehicle_id, part_id) DO UPDATE SET
                    changed_km=excluded.changed_km,
                    next_changed_km=excluded.next_changed_km,
                    changed_date=excluded.changed_date,
                    next_changed_date=excluded.next_changed_date
            """, (maintenance.vehicle_id, maintenance.part_id, maintenance.changed_km,
                  maintenance.next_changed_km, maintenance.changed_date, maintenance.next_changed_date))

    def get_details(self, keyword: str, active_user: str) -> list[VehicleMaintenanceDetail]:
        with self.db.get_session() as conn:
            rows = conn.execute("""
                SELECT v.id, v.car_no, v.model, v.company, v.onground_km,
                       c.part, m.changed_km, m.next_changed_km,
                       m.changed_date, m.next_changed_date
                FROM maintenance m
                JOIN vehicles v ON m.vehicle_id = v.id
                JOIN config c ON m.part_id = c.id
                WHERE v.active_user=? AND (v.car_no LIKE ? OR c.part LIKE ?)
                ORDER BY v.car_no
            """, (active_user, f"%{keyword}%", f"%{keyword}%")).fetchall()
            return [VehicleMaintenanceDetail(*row) for row in rows]