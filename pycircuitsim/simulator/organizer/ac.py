from .organizer import DataOrganizer
from . import handlers

class AcDataOrganizer(DataOrganizer):
    """DataOrganizer for AC simulations."""

    def build_handler_chain(self):
        voltage_handler = handlers.DefaultHandler(key="voltages")
        current_handler = handlers.CurrentHandler(key="currents", successor=voltage_handler)
        parameter_handler = handlers.ParameterHandler(key="parameters", successor=current_handler)
        frequency_handler = handlers.FrequencyHandler(key="frequency", successor=parameter_handler)
        return frequency_handler

    @property
    def frequency(self):
        return self.data.get('frequency', None)

    @property
    def currents(self):
        return self.data.get('currents', {})

    @property
    def voltages(self):
        return self.data.get('voltages', {})

    @property
    def parameters(self):
        return self.data.get('parameters', {})
