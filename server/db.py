import logging
import sqlite3

import numpy as np
import sqlite_vec

logger = logging.getLogger(__name__)


class Database:
    _instance = None

    def __init__(self, db_file: str = "database.sqlite"):
        self.db_file = db_file
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.enable_load_extension(True)
            sqlite_vec.load(self.conn)
            self.conn.enable_load_extension(False)
            logger.info("Vector Database file created.")
        except sqlite3.Error as e:
            logger.error(f"Error initializing the database: {e}")
            raise

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            logger.info("SQLite Vector Database initialized.")
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_tables(self) -> None:
        """Create required tables if they do not exist."""
        try:
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
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            self.conn.rollback()

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
        try:
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
                (img_emb.astype(np.float32),),
            )
            self.conn.commit()
            logger.info("Entry inserted into Vector Database.")
        except sqlite3.Error as e:
            logger.error(f"Error inserting entry: {e}")
            self.conn.rollback()
        except ValueError as e:
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
        try:
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
        except ValueError as e:
            logger.error("The model or processor may not have been loaded properly.")
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {e}")
            raise
    
    def test(self):
            x = self.conn.execute(
                """
                SELECT count(*) FROM vec_idx
                """)
            print(x.fetchall())

    def get_last_entry(self) -> tuple[bytes, str] | None:
        """
        Get last entry ordered by timestamp.

        Returns:
            tuple | None: A tuple of (raw bytes (embeddings), image path) or `None` if the database is empty.
        """
        try:
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


if __name__ == "__main__":
    db = Database()
    db.test()