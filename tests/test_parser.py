
import unittest
from unittest.mock import patch, Mock

from src.parser import ForumParser
from src.database import DatabaseRepository


class TestForumParser(unittest.TestCase):

    def setUp(self):
        self.parser = ForumParser()
        self.database = DatabaseRepository(":memory:")

        path = "tests/forum.html"
        with open(path, encoding="utf-8") as file:
            self.html = file.read()

    def test_parse_page(self):
        response = Mock()
        response.text = self.html

        with patch("src.parser.requests.get", return_value=response):
            result = self.parser.parse_page(
                "https://example.com",
                self.database
            )
        self.assertEqual(len(result), 2)

    def test_save_to_database(self):
        response = Mock()
        response.text = self.html

        with patch("src.parser.requests.get", return_value=response):
            result = self.parser.parse_page(
                "https://example.com",
                self.database
            )

        post_id = result[0]["id"]
        saved_post = self.database.get_by_id(post_id)

        self.assertIsNotNone(saved_post)
        self.assertEqual(saved_post["name"], "Ivan")

if __name__ == "__main__":
    unittest.main()
