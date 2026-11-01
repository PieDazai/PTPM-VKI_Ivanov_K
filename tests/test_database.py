import unittest
import sqlite3

from src.database import DatabaseRepository

class TestDatabaseRepository(unittest.TestCase):

    def setUp(self):
        self.repository = DatabaseRepository(":memory:")

    def test_add_success(self):
        result = self.repository.add(
            "1rwf4t2fdwqd",
            "Ivan",
            "<p>Первое сообщение</p>"
        )
        self.assertTrue(result)

    def test_add_duplicate_id(self):
        self.repository.add("1rwf4t2fdwqd", "Ivan", "Первое сообщение")

        with self.assertRaises(sqlite3.IntegrityError):
            self.repository.add("1rwf4t2fdwqd", "Petr", "Второе сообщение")

    def test_get_by_id_found(self):
        self.repository.add("1rwf4t2fdwqd", "Ivan", "Текст сообщения")

        result = self.repository.get_by_id("1rwf4t2fdwqd")

        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "1rwf4t2fdwqd")
        self.assertEqual(result["name"], "Ivan")
        self.assertEqual(result["message"], "Текст сообщения")

    def test_get_by_id_not_found(self):
        result = self.repository.get_by_id("23к23к")
        self.assertIsNone(result)

    def test_get_by_name_found(self):
        self.repository.add("1rwf4t2fdwqdtt", "Ivan", "Первое сообщение")
        self.repository.add("1rwf4t2fdwqd242", "Ivan", "Второе сообщение")
        self.repository.add("1rwf4t2fdwqdkjh", "Petr", "Сообщение Петра")

        result = self.repository.get_by_name("Ivan")

        self.assertEqual(len(result), 2)

    def test_get_by_name_not_found(self):
        result = self.repository.get_by_name("5tfgrvd")
        self.assertEqual(result, [])

    def test_update_success(self):
        self.repository.add("1rwf4t2fdwqdtt", "Ivan", "Старый текст")

        result = self.repository.update("1rwf4t2fdwqdtt", "Новый текст")

        self.assertTrue(result)

        comment = self.repository.get_by_id("1rwf4t2fdwqdtt")
        self.assertEqual(comment["message"], "Новый текст")

    def test_update_not_found(self):
        result = self.repository.update("6t45grt", "Новый текст")
        self.assertFalse(result)

    def test_delete_success(self):
        self.repository.add("1rwf4t2fdwqdtt", "Ivan", "Текст сообщения")

        result = self.repository.delete("1rwf4t2fdwqdtt")

        self.assertTrue(result)
        self.assertIsNone(self.repository.get_by_id("1rwf4t2fdwqdtt"))

    def test_delete_not_found(self):
        result = self.repository.delete("gfdgfdgd")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()