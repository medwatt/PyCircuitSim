from abc import ABC, abstractmethod

class MessageHandler(ABC):
    @abstractmethod
    def handle(self, msg_type: str, message: str) -> None:
        pass
