from calculator import TriangleCalculator
from database import TriangleDatabase
from user_io import ConsoleUserIO
from notifier import EmailNotifier
from controller import TriangleController
def main():
    # Для тестов используется :memory:, а для реальной работы создастся файл triangles.db
    controller = TriangleController(
        calc=TriangleCalculator(),
        db=TriangleDatabase("triangles.db"),
        user_io=ConsoleUserIO(),
        notifier=EmailNotifier(),
    )
    result, source = controller.run()
    print(f"\nРезультат ({source}): {result}")
if __name__ == "__main__":
    main()