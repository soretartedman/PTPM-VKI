class TriangleCalculator:

    def calculate(self, a: float, b: float, c: float) -> tuple[str, str]:
        if a <= 0 or b <= 0 or c <= 0:
            return "", "Стороны должны быть положительными числами"
        if a + b <= c or a + c <= b or b + c <= a:
            return "", "Треугольник с такими сторонами не существует"
        if a == b == c:
            return "равносторонний", ""
        if a == b or a == c or b == c:
            return "равнобедренный", ""
        return "разносторонний", ""