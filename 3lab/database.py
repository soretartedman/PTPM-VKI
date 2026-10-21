import sqlite3
class TriangleDatabase:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                a REAL NOT NULL,
                b REAL NOT NULL,
                c REAL NOT NULL,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (a, b, c)
            )
        """)
        self.conn.commit()
    def add(self, a: float, b: float, c: float, triangle_type: str, error_message: str) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO triangles (a, b, c, triangle_type, error_message) VALUES (?, ?, ?, ?, ?)",
            (a, b, c, triangle_type, error_message),
        )
        self.conn.commit()
    def get(self, a: float, b: float, c: float):
        cur = self.conn.execute(
            "SELECT triangle_type, error_message FROM triangles WHERE a=? AND b=? AND c=?",
            (a, b, c),
        )
        return cur.fetchone()
    def delete(self, a: float, b: float, c: float) -> None:
        self.conn.execute("DELETE FROM triangles WHERE a=? AND b=? AND c=?", (a, b, c))
        self.conn.commit()
    def close(self) -> None:
        self.conn.close()