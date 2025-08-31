import logging
import sqlite3
import threading

import numpy as np
import sqlite_vec

logger = logging.getLogger(__name__)


class Database:
    _instance = None
    _lock = threading.Lock()

    def __init__(self, db_file: str = "database.sqlite"):
        self.db_file = db_file
        self.thread_local = threading.local()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                logger.info("SQLite Vector Database singleton created.")
                cls._instance = super().__new__(cls)
        return cls._instance

    def _get_connection(self):
        """Get a thread-local database connection."""
        if not hasattr(self.thread_local, "conn"):
            try:
                conn = sqlite3.connect(self.db_file)
                conn.enable_load_extension(True)
                sqlite_vec.load(conn)
                conn.enable_load_extension(False)
                self.thread_local.conn = conn
                logger.info(f"New DB connection for thread {threading.get_ident()}")
            except sqlite3.Error as e:
                logger.error(f"Error initializing the database connection: {e}")
                raise
        return self.thread_local.conn

    def create_tables(self) -> None:
        """Create required tables if they do not exist."""
        conn = self._get_connection()
        try:
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS img_info (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        image_path TEXT NOT NULL,
                        application_name TEXT,
                        timestamp TIMESTAMP NOT NULL
                    );
                """
            )
            conn.execute(
                """
                    CREATE VIRTUAL TABLE IF NOT EXISTS vec_idx USING vec0 (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        embedding FLOAT[768] distance_metric=cosine
                    );
                """
            )
            conn.commit()
            logger.info("Tables created.")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            conn.rollback()

    def insert_entry(
        self,
        image_path: str,
        img_emb: np.ndarray,
        application_name: str = "",
    ) -> None:
        """
        Insert an image entry to the database using an image path or the image embedding if provided.

        Args:
            image_path (str): The image path.
            application_name (str): The application name.
            embedding (np.ndarray, optional): The image embedding.
        """
        conn = self._get_connection()
        try:
            conn.execute(
                """
                    INSERT INTO img_info (image_path, application_name, timestamp)
                    VALUES (?, ?, datetime('now'))
                """,
                (
                    image_path,
                    application_name,
                ),
            )
            conn.execute(
                """
                    INSERT INTO vec_idx (embedding)
                    VALUES (?)
                """,
                (img_emb.astype(np.float32),),
            )
            conn.commit()
            logger.info("Entry inserted into Vector Database.")
        except sqlite3.Error as e:
            logger.error(f"Error inserting entry: {e}")
            conn.rollback()
        except ValueError:
            logger.error("The model or processor may not have been loaded properly.")
        except Exception as e:
            logger.error(f"Unexpected error while inserting entry: {e}")
            raise

    def get_top_k_entries(
        self, text_emb: np.ndarray, k: int
    ) -> list[tuple[str, str, str, float]] | None:
        """
        Get top k similar image entries given a text query.

        Args:
            query (str): Text query against which the top `k` similar images are retrieved.
            k (int): Number of images to retrieve from the database.
        Returns:
            tuple | None: A tuple having info of top k entries or None if the database is empty.
        """
        conn = self._get_connection()
        try:
            top_k_entries = conn.execute(
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
                (text_emb.astype(np.float32), k),
            ).fetchall()
            if top_k_entries:
                logger.info(f"Fetched top {k} entries from the database.")
            else:
                logger.warning("No entries found matching the query.")
            return top_k_entries
        except sqlite3.Error as e:
            logger.error(f"Error fetching top {k} entries: {e}")
            return None
        except ValueError:
            logger.error("The model or processor may not have been loaded properly.")
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {e}")
            raise

    def get_last_entry(self) -> tuple[bytes, str] | None:
        """
        Get last entry ordered by timestamp.

        Returns:
            tuple | None: A tuple of (raw bytes (embeddings), image path) or `None` if the database is empty.
        """
        conn = self._get_connection()
        try:
            last_entry = conn.execute(
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
                logger.info("Returned the last entry pushed to the Vector Database.")
            else:
                logger.warning("No entries found in the database.")
            return last_entry
        except sqlite3.Error as e:
            logger.error(f"Error retrieving the last entry: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching the last entry: {e}")
            raise

    def purge_entries(self) -> None:
        """
        Purge all entries from the database.

        Clears all records from both `img_info` and `vec_idx` tables.
        """
        conn = self._get_connection()
        try:
            conn.execute("DELETE FROM img_info;")
            conn.execute("DELETE FROM vec_idx;")
            conn.commit()
            logger.info("All entries purged from the database.")
        except sqlite3.Error as e:
            logger.error(f"Error purging entries: {e}")
            conn.rollback()
        except Exception as e:
            logger.error(f"Unexpected error during purge: {e}")
            raise


if __name__ == "__main__":
    db = Database()
