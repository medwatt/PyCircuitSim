# imports <<<
from abc import ABC, abstractmethod
# >>>


# Abstract Class: Component <<<
class Component(ABC):
    @property
    @abstractmethod
    def spice_prefix(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
# >>>


# Class: TwoTerminalComponent <<<
class TwoTerminalComponent(Component):
    def __init__(self, id: str, nodes: tuple[str, str], value: str, **params):
        """
        Spice Two-terminal component.

        Args:
            id: Unique identifier for the component.
            nodes: (plus_node, minus_node)
            value: Value.
        """
        self.id = id
        self.nodes = nodes
        self.value = value
        self.params = params

    def __str__(self):
        params_str = " ".join(f"{k}={v}" for k, v in self.params.items())
        prefix = self.spice_prefix
        return f'{prefix}{self.id} {" ".join(self.nodes)} {self.value} {params_str}'.strip()

    @property
    @abstractmethod
    def spice_prefix(self) -> str:
        pass
# >>>
