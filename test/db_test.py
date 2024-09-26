import unittest

import numpy as np

from db import create_connection, create_entry, create_table, get_all_entries


class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        # Set up an in-memory SQLite database
        self.conn = create_connection(":memory:")
        create_table(self.conn)

    def tearDown(self):
        # Close the connection after each test
        self.conn.close()

    def test_create_table(self):
        # Check if the table 'entries' exists
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='entries';"
        )
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

    def test_create_entry(self):
        # Create a random vector and insert into the table
        image_path = "test_image.jpg"
        vector = np.random.rand(128).astype(np.float32)
        create_entry(self.conn, image_path, vector)

        # Verify if the entry was added
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM entries;")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_get_all_entries(self):
        # Insert multiple entries
        vectors = [np.random.rand(128).astype(np.float32) for _ in range(3)]
        image_paths = [f"image_{i}.jpg" for i in range(3)]
        for i in range(3):
            create_entry(self.conn, image_paths[i], vectors[i])

        # Retrieve all entries
        entries = get_all_entries(self.conn)

        # Validate the number of entries and content
        self.assertEqual(len(entries), 3)
        for i in range(3):
            self.assertEqual(entries[i]["image_path"], image_paths[i])
            np.testing.assert_array_almost_equal(entries[i]["vector"], vectors[i])


if __name__ == "__main__":
    unittest.main()
