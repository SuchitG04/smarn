import sqlite3
import sqlite_vec
import numpy as np
import logging

from .vectors import get_img_emb, get_text_emb

logger = logging.getLogger(__name__)

class Database:
    _instance = None

    def __init__(self, db_file: str = "database.sqlite"):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.conn.enable_load_extension(True)
        sqlite_vec.load(self.conn)
        self.conn.enable_load_extension(False)
        logger.info("Vector Database file created.")

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            logger.info("SQLite Vector Database initialized.")
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_tables(self) -> None:
        """Create required tables if they do not exist."""
        self.conn.execute(
            """
                CREATE TABLE IF NOT EXISTS img_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path TEXT NOT NULL,
                    application_name TEXT,
                    timestamp TIMESTAMP NOT NULL
                );
            """
        )
        self.conn.execute(
            """
                CREATE VIRTUAL TABLE IF NOT EXISTS vec_idx USING vec0 (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    embedding FLOAT[768] distance_metric=cosine
                );
            """
        )
        self.conn.commit()
        logger.info("Tables created.")

    def insert_entry(self, image_path: str, application_name: str = "", embedding: np.ndarray | None = None) -> None:
        """
        Insert an image entry to the database using an image path or the image embedding if provided.

        Args:
            image_path (str): The image path.
            application_name (str): The application name.
            embedding (np.ndarray, optional): The image embedding.
        """
        if embedding is None:
            embedding = get_img_emb(image_path)

        self.conn.execute(
            """
                INSERT INTO img_info (image_path, application_name, timestamp)
                VALUES (?, ?, datetime())
            """,
            (
                image_path,
                application_name,
            ),
        )
        self.conn.execute(
            """
                INSERT INTO vec_idx (embedding)
                VALUES (?)
            """,
            (embedding,),
        )
        self.conn.commit()
        logger.info("Entry inserted into Vector Database.")

    def get_top_k_entries(self, query: str, k: int) -> list[tuple[str, str, str, float]] | None:
        """
        Get top k similar image entries given a text query.

        Args:
            query (str): Text query against which the top `k` similar images are retrieved.
            k (int): Number of images to retrieve from the database.
        Returns:
            tuple | None: A tuple having info of top k entries or None if the database is empty.
        """
        text_emb = get_text_emb(query)
        top_k_entries = self.conn.execute(
            """
                SELECT
                    img_info.image_path,
                    img_info.application_name,
                    img_info.timestamp,
                    distance
                FROM vec_idx
                LEFT JOIN img_info ON vec_idx.id = img_info.id
                WHERE embedding MATCH ?
                    AND k = ?
                ORDER BY distance
            """,
            (text_emb, k),
        ).fetchall()
        logger.info(f"Fetched top {k} entries from the database.")
        return top_k_entries

    def get_last_entry(self) -> tuple[bytes, str] | None:
        """
        Get last entry ordered by timestamp.

        Returns:
            tuple | None: A tuple of (raw bytes (embeddings), image path) or `None` if the database is empty.
        """
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
        logger.info("Returned the last entry pushed to the Vector Database.")
        return last_entry