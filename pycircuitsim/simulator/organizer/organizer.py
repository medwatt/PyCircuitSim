from abc import abstractmethod

class DataOrganizer:
    """Base class to organize ngspice data."""

    def __init__(self):
        self.data = {}
        self.handler_chain = self.build_handler_chain()

    @abstractmethod
    def build_handler_chain(self):
        pass

    def add_data(self, vector_name, data):
        self.handler_chain.handle(vector_name, data, self)
