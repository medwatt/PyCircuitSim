import re
from .base import MessageHandler

_DEFAULT_FILTER_PATTERNS = [
    r"Using \w+ \d+(\.\d+)? as \w+",
]

class StderrHandler(MessageHandler):
    def __init__(self, filter_patterns=None):
        patterns = filter_patterns if filter_patterns is not None else _DEFAULT_FILTER_PATTERNS
        self.filter_patterns = [re.compile(p) for p in patterns]

    def handle(self, msg_type: str, message: str) -> None:
        if msg_type == 'stderr':
            if any(pattern.search(message) for pattern in self.filter_patterns):
                return
            print(f"STDERR: {message}")
