# api/db.py
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "complaints.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT NOT NULL,
            complaint_details TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(phone_number, complaint_details)
        )
    """)
    conn.commit()
    conn.close()

init_db()


def insert_complaint(data: dict) -> str:
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Check for duplicate
        c.execute("""
            SELECT complaint_id FROM complaints
            WHERE phone_number = ? AND complaint_details = ?
        """, (data["phone_number"], data["complaint_details"]))
        existing = c.fetchone()

        if existing:
            return existing[0]  # Return existing complaint ID

        c.execute("""
            INSERT INTO complaints (complaint_id, name, phone_number, email, complaint_details, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["complaint_id"],
            data["name"],
            data["phone_number"],
            data["email"],
            data["complaint_details"],
            data["created_at"]
        ))
        conn.commit()
        return data["complaint_id"]
    finally:
        conn.close()

def get_complaint_by_id(complaint_id_or_phone: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if complaint_id_or_phone.upper().startswith("CMP"):
        c.execute("SELECT * FROM complaints WHERE complaint_id = ?", (complaint_id_or_phone,))
    else:
        c.execute("""
            SELECT * FROM complaints
            WHERE phone_number = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (complaint_id_or_phone,))
    row = c.fetchone()
    conn.close()
    return {key.strip().lower(): row[key] for key in row.keys()} if row else None
