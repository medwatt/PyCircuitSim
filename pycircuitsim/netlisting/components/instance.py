from .base import Component


# Class: SubCircuitInstance <<<
class SubCircuitInstance(Component):
    def __init__(self, id: str, nodes: tuple[str, ...], subcircuit, params: dict = {}, copy: bool = False):
        """
        Spice subcircuit instance component (X element).

        Args:
            id: Unique identifier for the subcircuit instance.
            nodes: Tuple of nodes connecting to the subcircuit.
            subcircuit: Reference to the subcircuit definition.
            params: Dictionary of parameter values for the subcircuit (optional).
            copy: If True, creates a uniquely-named copy of the subcircuit (optional).
        """
        self.id = id
        self.nodes = nodes
        self.subcircuit = subcircuit
        self.params = params or {}
        self.copy = copy

    @property
    def spice_prefix(self):
        return "X"

    def __str__(self):
        subckt_name = self.subcircuit.name
        if self.copy:
            subckt_name += f"_{self.id}"
        params_str = " ".join(f"{k}={v}" for k, v in self.params.items())
        return f'{self.spice_prefix}{self.id} {" ".join(self.nodes)} {subckt_name} {params_str}'.strip()
# >>>


# Class: OsdiInstance <<<
class OsdiInstance(Component):
    def __init__(self, id: str, nodes: tuple[str, ...], model_name: str, params: dict = {}):
        """
        Spice OSDI (Open Source Device Interface) instance component (N element).

        Args:
            id: Unique identifier for the instance.
            nodes: Tuple of nodes connecting to the component.
            model_name: Name of the OSDI model.
            params: Dictionary of parameter values (optional).
        """
        self.id = id
        self.nodes = nodes
        self.model_name = model_name
        self.params = params or {}

    @property
    def spice_prefix(self):
        return "N"

    def __str__(self):
        params_str = " ".join(f"{k}={v}" for k, v in self.params.items())
        return f'{self.spice_prefix}{self.id} {" ".join(self.nodes)} {self.model_name} {params_str}'.strip()
# >>>
