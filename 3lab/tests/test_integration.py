import unittest
from unittest.mock import MagicMock
from calculator import TriangleCalculator
from database import TriangleDatabase
from controller import TriangleController


class TestControllerIntegration(unittest.TestCase):
    """Интеграционные тесты: Controller + Calculator + DB + моки."""

    def setUp(self):
        self.calc = TriangleCalculator()
        self.db = TriangleDatabase()          # реальная БД (in-memory)
        self.user_io = MagicMock()            # заглушка ввода
        self.notifier = MagicMock()           # заглушка отправки
        self.notifier.send.return_value = True
        self.controller = TriangleController(
            self.calc, self.db, self.user_io, self.notifier
        )

    def tearDown(self):
        self.db.close()

    def test_new_data_computed_saved_and_sent(self):
        """1. Нет в БД → вычисление + сохранение + отправка."""
        self.user_io.get_sides.return_value = (3, 4, 5)
        result, source = self.controller.run()

        self.assertEqual(source, "вычисление")
        self.assertIn("разносторонний", result)
        self.assertEqual(self.db.get(3, 4, 5), ("разносторонний", ""))
        self.notifier.send.assert_called_once_with(result)

    def test_existing_data_taken_from_db(self):
        """2. Уже в БД → берём из БД, calculate не вызывается."""
        self.db.add(3, 3, 3, "равносторонний", "")
        self.user_io.get_sides.return_value = (3, 3, 3)

        self.controller.calc = MagicMock()
        result, source = self.controller.run()

        self.assertEqual(source, "БД")
        self.assertIn("равносторонний", result)
        self.controller.calc.calculate.assert_not_called()
        self.notifier.send.assert_called_once()

    def test_invalid_triangle_error_saved_and_sent(self):
        """3. Ошибочный ввод → ошибка сохраняется в БД и отправляется."""
        self.user_io.get_sides.return_value = (1, 2, 10)
        result, source = self.controller.run()

        self.assertEqual(source, "вычисление")
        self.assertIn("не существует", result)
        self.assertEqual(
            self.db.get(1, 2, 10),
            ("", "Треугольник с такими сторонами не существует")
        )
        self.notifier.send.assert_called_once_with(result)

    def test_second_run_uses_cache(self):
        """4. Повторный запуск с теми же данными → второй раз из БД."""
        self.user_io.get_sides.return_value = (6, 6, 8)

        r1, s1 = self.controller.run()
        r2, s2 = self.controller.run()

        self.assertEqual(s1, "вычисление")
        self.assertEqual(s2, "БД")
        self.assertEqual(r1, r2)
        self.assertEqual(self.notifier.send.call_count, 2)