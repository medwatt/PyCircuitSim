from .base import MessageHandler

class StdoutHandler(MessageHandler):
    def handle(self, msg_type: str, message: str) -> None:
        if msg_type == 'stdout':
            pass
            # print(f"STDOUT: {message}")
