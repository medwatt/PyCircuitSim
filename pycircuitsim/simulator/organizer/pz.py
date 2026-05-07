from .organizer import DataOrganizer
from . import handlers

class PzDataOrganizer(DataOrganizer):
    """DataOrganizer for Pole-Zero simulations."""

    def build_handler_chain(self):
        pole_zero_handler = handlers.PoleZeroHandler(key="pole_zero")
        return pole_zero_handler

    @property
    def zero_pole(self):
        return self.data.get('pole_zero', {})
