import sqlite_vec
import sqlite3

from sqlite_vec import serialize_float32
from vec_emb import get_img_emb
from textwrap import dedent


class Database:
    def __init__(self, db_file):
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
        last_entry = self.conn.execute(
            """
                SELECT * FROM img_info
                ORDER BY timestamp DESC 
                LIMIT 1;
            """
        ).fetchone()
        if last_entry:
            return last_entry
        else:
            return None

