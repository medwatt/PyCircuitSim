from .organizer import DataOrganizer
from . import handlers

class SensDataOrganizer(DataOrganizer):
    """DataOrganizer for Sensitivity simulations."""

    def build_handler_chain(self):
        sensitivity_handler = handlers.DefaultHandler(key="sensitivities")
        return sensitivity_handler

    @property
    def sensitivities(self):
        return self.data.get('sensitivities', {})
