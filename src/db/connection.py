import sqlite3
from pathlib import Path

def get_connection(db_path):
    # Ensures database directory exists and enforces SQLite foreign key constraints
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON;")

    return conn
