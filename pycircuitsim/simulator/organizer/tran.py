from .organizer import DataOrganizer
from . import handlers

class TranDataOrganizer(DataOrganizer):
    """DataOrganizer for Transient simulations."""

    def build_handler_chain(self):
        voltage_handler = handlers.DefaultHandler(key="voltages")
        current_handler = handlers.CurrentHandler(key="currents", successor=voltage_handler)
        parameter_handler = handlers.ParameterHandler(key="parameters", successor=current_handler)
        time_handler = handlers.TimeHandler(key="time", successor=parameter_handler)
        return time_handler

    @property
    def time(self):
        return self.data.get("time", {})

    @property
    def currents(self):
        return self.data.get("currents", {})

    @property
    def voltages(self):
        return self.data.get("voltages", {})

    @property
    def parameters(self):
        return self.data.get("parameters", {})
