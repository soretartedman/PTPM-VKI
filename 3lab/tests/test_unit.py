import unittest
import sys
import os
from unittest.mock import patch

# Добавляем путь к папке 3lab, чтобы импорты работали 100%
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import TriangleDatabase
from user_io import ConsoleUserIO


class TestDatabaseUnit(unittest.TestCase):
    def setUp(self):
        self.db = TriangleDatabase()

    def tearDown(self):
        self.db.close()

    def test_add_and_get(self):
        self.db.add(3, 4, 5, "разносторонний", "")
        self.assertEqual(self.db.get(3, 4, 5), ("разносторонний", ""))

    def test_delete(self):
        self.db.add(3, 4, 5, "разносторонний", "")
        self.db.delete(3, 4, 5)
        self.assertIsNone(self.db.get(3, 4, 5))


class TestConsoleUserIOUnit(unittest.TestCase):
    @patch("builtins.input", side_effect=["3", "4", "5"])
    def test_get_sides_mocked_input(self, mock_input):
        io = ConsoleUserIO()
        self.assertEqual(io.get_sides(), (3.0, 4.0, 5.0))
        self.assertEqual(mock_input.call_count, 3)