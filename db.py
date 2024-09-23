import datetime
import sqlite3
from typing import List

import numpy as np
import sqlite_vec


def create_connection(db_file: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_file)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    return conn


# TODO: Add window title and application name
def create_table(conn: sqlite3.Connection) -> None:
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT NOT NULL,
        vector_embedding float[] NOT NULL,
        timestamp TEXT NOT NULL
    );
    """
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()


# not sure about the type of vector_embedding using float[] for now
def create_entry(conn: sqlite3.Connection, image_path: str, vector: np.ndarray) -> None:
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO entries (image_path, vector_embedding, timestamp) 
        VALUES (?, ?, ?)
    """,
        (image_path, vector, timestamp),
    )
    conn.commit()


def get_all_entries(conn: sqlite3.Connection) -> List[dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT id, image_path, vector_embedding, timestamp FROM entries;")
    rows = cursor.fetchall()
    results = []
    for row in rows:
        vector = np.frombuffer(row[2], dtype=np.float32)
        results.append(
            {"id": row[0], "image_path": row[1], "vector": vector, "timestamp": row[3]}
        )
    return results
