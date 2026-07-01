#part_repository.py
from db_connection import DatabaseConnection
from models import PartConfig

class PartRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db
        self._create_table()

    def _create_table(self):
        with self.db.get_session() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS config(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    part TEXT NOT NULL UNIQUE,
                    km_life INTEGER NOT NULL,
                    month_life INTEGER NOT NULL,
                    km_limit INTEGER NOT NULL,
                    day_limit INTEGER NOT NULL
                )
            """)

    def save(self, part_config: PartConfig):
        with self.db.get_session() as conn:
            cur = conn.cursor()
            if part_config.id is None:
                cur.execute("""
                    INSERT INTO config (part, km_life, month_life, km_limit, day_limit)
                    VALUES (?,?,?,?,?)
                """, (part_config.part, part_config.km_life, part_config.month_life,
                      part_config.km_limit, part_config.day_limit))
                part_config.id = cur.lastrowid
            else:
                cur.execute("""
                    UPDATE config
                    SET km_life=?, month_life=?, km_limit=?, day_limit=?
                    WHERE id=?
                """, (part_config.km_life, part_config.month_life,
                      part_config.km_limit, part_config.day_limit, part_config.id))

    def load_all(self) -> list[PartConfig]:
        with self.db.get_session() as conn:
            rows = conn.execute(
                "SELECT id, part, km_life, month_life, km_limit, day_limit FROM config"
            ).fetchall()
            return [PartConfig(*row) for row in rows]

    def get_by_name(self, part_name: str) -> PartConfig | None:
        with self.db.get_session() as conn:
            row = conn.execute(
                "SELECT id, part, km_life, month_life, km_limit, day_limit FROM config WHERE part=?",
                (part_name,)
            ).fetchone()
            return PartConfig(*row) if row else None

    def delete(self, part_config: PartConfig):
        with self.db.get_session() as conn:
            conn.execute("DELETE FROM config WHERE id=?", (part_config.id,))