class TriangleController:
    """Бизнес-логика сквозного сценария."""

    def __init__(self, calc, db, user_io, notifier):
        self.calc = calc
        self.db = db
        self.user_io = user_io
        self.notifier = notifier
    def run(self) -> tuple[str, str]:
        a, b, c = self.user_io.get_sides()
        cached = self.db.get(a, b, c)
        if cached is not None:
            triangle_type, error = cached
            source = "БД"
        else:
            triangle_type, error = self.calc.calculate(a, b, c)
            self.db.add(a, b, c, triangle_type, error)
            source = "вычисление"
        if error:
            result = f"Ошибка: {error}"
        else:
            result = f"Тип треугольника: {triangle_type}"
        self.notifier.send(result)
        return result, source