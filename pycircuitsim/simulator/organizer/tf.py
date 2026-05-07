from .organizer import DataOrganizer
from . import handlers

class TfDataOrganizer(DataOrganizer):
    """DataOrganizer for Transfer Function simulations."""

    def build_handler_chain(self):
        transfer_function_handler = handlers.TransferFunctionHandler(key="transfer_function")
        impedance_handler = handlers.ImpedanceHandler(key="impedances", successor=transfer_function_handler)
        return impedance_handler

    @property
    def impedances(self):
        return self.data.get('impedances', {})

    @property
    def transfer_function(self):
        return self.data.get('transfer_function', None)
