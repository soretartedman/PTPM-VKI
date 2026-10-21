from abc import ABC, abstractmethod
class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> bool:
        ...
class EmailNotifier(Notifier):
    def send(self, message: str) -> bool:
        print(f"[EMAIL SENT] {message}")
        return True