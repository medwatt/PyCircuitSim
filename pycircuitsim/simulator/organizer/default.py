from .organizer import DataOrganizer
from . import handlers

class DefaultDataOrganizer(DataOrganizer):
    """DataOrganizer for unrecognised simulation types."""

    def build_handler_chain(self):
        return handlers.DefaultHandler(key="others")

    @property
    def others(self):
        return self.data.get('others', {})
