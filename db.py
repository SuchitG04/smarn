import datetime
import os
import sqlite3
from typing import List

import numpy as np
import sqlite_vec

from vec_emb import get_img_emb


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
def create_entry(conn: sqlite3.Connection, image_path: str) -> None:
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    vector = get_img_emb(image_path)
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


def add_images_from_directory(conn: sqlite3.Connection, directory: str) -> None:
    for filename in os.listdir(directory):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(directory, filename)
            create_entry(conn, image_path)


def print_entries(conn: sqlite3.Connection) -> None:
    entries = get_all_entries(conn)
    for entry in entries:
        print(
            f"ID: {entry['id']}, Image Path: {entry['image_path']}, Timestamp: {entry['timestamp']}, Vector: {entry['vector']}"
        )


if __name__ == "__main__":
    db_file = "test.db"
    conn = create_connection(db_file)
    create_table(conn)

    add_images_from_directory(conn, "smarn_screenshots")

    print_entries(conn)

    conn.close()

