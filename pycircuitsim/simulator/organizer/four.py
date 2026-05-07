from .organizer import DataOrganizer
from . import handlers

class FourDataOrganizer(DataOrganizer):
    """DataOrganizer for Fourier simulations."""

    def build_handler_chain(self):
        spectra_handler = handlers.DefaultHandler(key="spectra")
        harmonic_handler = handlers.HarmonicHandler(key="harmonic", successor=spectra_handler)
        return harmonic_handler

    @property
    def harmonic(self):
        return self.data.get('harmonic', None)

    @property
    def spectra(self):
        return self.data.get('spectra', {})
