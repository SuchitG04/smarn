import sqlite_vec
import sqlite3

from sqlite_vec import serialize_float32
from vectors import get_img_emb
from textwrap import dedent

class Database:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.conn.enable_load_extension(True)
        sqlite_vec.load(self.conn)
        self.conn.enable_load_extension(False)

        version_info = self.conn.execute("SELECT sqlite_version(), vec_version()").fetchone()
        print(
            dedent(f"""
                Database initialized.
                vec_version(): {version_info[0]}
                sqlite_version(): {version_info[1]}
            """)
        )

    # TODO: Add window title and application name
    def create_tables(self) -> None:
        """Create required tables if they do not exist."""
        self.conn.execute(
            """
                CREATE TABLE IF NOT EXISTS img_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL
                );
            """
        )
        self.conn.execute(
            """
                CREATE VIRTUAL TABLE IF NOT EXISTS vec_idx USING vec0  (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    embedding FLOAT[768]
                );
            """
        )
        self.conn.commit()

    def insert_entry(self, image_path: str) -> None:
        """Insert an image entry to the database using an image path."""
        embedding = get_img_emb(image_path)
        self.conn.execute(
        """
                INSERT INTO img_info (image_path, timestamp) 
                VALUES (?, datetime())
            """,
            (image_path, ),
        )
        self.conn.execute(
            """
                INSERT INTO vec_idx (embedding)
                VALUES (?)
            """,
            (serialize_float32(embedding), ),
        )
        self.conn.commit()

    def get_last_entry(self) -> tuple | None:
        """Get last entry ordered by timestamp. Returns a tuple of (raw bytes embeddings, image path)."""
        last_entry = self.conn.execute(
            """
                SELECT
                    vec_idx.embedding,
                    img_info.image_path
                FROM vec_idx
                LEFT JOIN img_info ON vec_idx.id = img_info.id
                ORDER BY img_info.timestamp DESC 
                LIMIT 1;
            """
        ).fetchone()
        if last_entry:
            return last_entry
        else:
            return None
