import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "complaints.db")

# Ensure table exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            complaint TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Call init on module import
init_db()

def insert_complaint(data: dict):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO complaints (complaint_id, name, mobile, complaint, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["complaint_id"],
            data["name"],
            data["mobile"],
            data["complaint"],
            data["status"]
        ))
        conn.commit()
    finally:
        conn.close()

def get_complaint_by_id(complaint_id: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM complaints WHERE complaint_id = ?", (complaint_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def get_complaint_by_mobile(mobile: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM complaints WHERE mobile = ? ORDER BY ROWID DESC LIMIT 1", (mobile,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None
