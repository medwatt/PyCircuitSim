from .organizer import DataOrganizer
from .op import OpDataOrganizer
from .tran import TranDataOrganizer
from .ac import AcDataOrganizer
from .tf import TfDataOrganizer
from .pz import PzDataOrganizer
from .sens import SensDataOrganizer
from .four import FourDataOrganizer
from .default import DefaultDataOrganizer

class DataOrganizerFactory:
    """Factory to create DataOrganizer instances based on simulation type."""

    @staticmethod
    def create_data_organizer(simulation_type: str) -> DataOrganizer:
        organizers = {
            'op': OpDataOrganizer,
            'dc': OpDataOrganizer,
            'tran': TranDataOrganizer,
            'ac': AcDataOrganizer,
            'tf': TfDataOrganizer,
            'pz': PzDataOrganizer,
            'sens': SensDataOrganizer,
            'fourier': FourDataOrganizer,
        }
        organizer_class = organizers.get(simulation_type.lower(), DefaultDataOrganizer)
        return organizer_class()
