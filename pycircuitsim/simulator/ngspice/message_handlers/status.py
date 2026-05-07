from .base import MessageHandler

class StatusHandler(MessageHandler):
    def handle(self, msg_type: str, message: str) -> None:
        if msg_type == 'status':
            pass
            # print(f"STATUS: {message}")
