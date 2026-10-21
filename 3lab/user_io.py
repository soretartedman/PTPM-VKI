from abc import ABC, abstractmethod
class UserIO(ABC):
    @abstractmethod
    def get_sides(self) -> tuple[float, float, float]:
        ...
class ConsoleUserIO(UserIO):

    def get_sides(self) -> tuple[float, float, float]:
        a = float(input("Введите сторону a: "))
        b = float(input("Введите сторону b: "))
        c = float(input("Введите сторону c: "))
        return a, b, c