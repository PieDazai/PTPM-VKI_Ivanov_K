
import unittest
import sqlite3

from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):

    def setUp(self):
        self.repository = DatabaseRepository(":memory:")

    def test_add_success(self):
        result = self.repository.add(
            101,
            "Ivan",
            "<p>Первое сообщение</p>"
        )
        self.assertTrue(result)

    def test_add_duplicate_id(self):
        self.repository.add(101, "Ivan", "Первое сообщение")

        with self.assertRaises(sqlite3.IntegrityError):
            self.repository.add(101, "Petr", "Второе сообщение")

    def test_get_by_id_found(self):
        self.repository.add(101, "Ivan", "Текст сообщения")

        result = self.repository.get_by_id(101)

        self.assertIsNotNone(result)
        self.assertEqual(result["id"], 101)
        self.assertEqual(result["name"], "Ivan")
        self.assertEqual(result["message"], "Текст сообщения")

    def test_get_by_id_not_found(self):
        result = self.repository.get_by_id(999)
        self.assertIsNone(result)

    def test_get_by_name_found(self):
        self.repository.add(101, "Ivan", "Первое сообщение")
        self.repository.add(102, "Ivan", "Второе сообщение")
        self.repository.add(103, "Petr", "Сообщение Петра")

        result = self.repository.get_by_name("Ivan")

        self.assertEqual(len(result), 2)

    def test_get_by_name_not_found(self):
        result = self.repository.get_by_name("Unknown")
        self.assertEqual(result, [])

    def test_update_success(self):
        self.repository.add(101, "Ivan", "Старый текст")

        result = self.repository.update(101, "Новый текст")

        self.assertTrue(result)

        comment = self.repository.get_by_id(101)
        self.assertEqual(comment["message"], "Новый текст")

    def test_update_not_found(self):
        result = self.repository.update(999, "Новый текст")
        self.assertFalse(result)

    def test_delete_success(self):
        self.repository.add(101, "Ivan", "Текст сообщения")

        result = self.repository.delete(101)

        self.assertTrue(result)
        self.assertIsNone(self.repository.get_by_id(101))

    def test_delete_not_found(self):
        result = self.repository.delete(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
