from .base import Component, TwoTerminalComponent


# Class: Resistor <<<
class Resistor(TwoTerminalComponent):
    @property
    def spice_prefix(self):
        return "R"
# >>>


# Class: Inductor <<<
class Inductor(TwoTerminalComponent):
    @property
    def spice_prefix(self):
        return "L"
# >>>


# Class: Capacitor <<<
class Capacitor(TwoTerminalComponent):
    @property
    def spice_prefix(self):
        return "C"
# >>>


# Class: MutualInductance <<<
class MutualInductance(Component):
    def __init__(self, id: str, inductor1: str, inductor2: str, coupling: str):
        """
        Spice mutual inductance between two inductors (K element).

        Args:
            id: Unique identifier for the mutual inductance.
            inductor1: ID of the first inductor (without L prefix).
            inductor2: ID of the second inductor (without L prefix).
            coupling: Coupling coefficient (0 < k ≤ 1).
        """
        self.id = id
        self.inductor1 = inductor1
        self.inductor2 = inductor2
        self.coupling = coupling

    @property
    def spice_prefix(self):
        return "K"

    def __str__(self):
        return f"{self.spice_prefix}{self.id} L{self.inductor1} L{self.inductor2} {self.coupling}"
# >>>


# Class: VoltageControlledSwitch <<<
class VoltageControlledSwitch(Component):
    def __init__(self, id: str, nodes: tuple[str, str, str, str], model_name: str, initial_state: str = ""):
        """
        Spice voltage-controlled switch (S element).

        Args:
            id: Unique identifier for the switch.
            nodes: (n+, n-, nc+, nc-).
            model_name: Name of the switch model.
            initial_state: Initial state, "on" or "off" (optional).
        """
        self.id = id
        self.nodes = nodes
        self.model_name = model_name
        self.initial_state = initial_state

    @property
    def spice_prefix(self):
        return "S"

    def __str__(self):
        parts = [f"{self.spice_prefix}{self.id}", " ".join(self.nodes), self.model_name]
        if self.initial_state:
            parts.append(self.initial_state)
        return " ".join(parts)
# >>>


# Class: CurrentControlledSwitch <<<
class CurrentControlledSwitch(Component):
    def __init__(self, id: str, nodes: tuple[str, str], source_name: str, model_name: str, initial_state: str = ""):
        """
        Spice current-controlled switch (W element).

        Args:
            id: Unique identifier for the switch.
            nodes: (n+, n-).
            source_name: Name of the controlling voltage source.
            model_name: Name of the switch model.
            initial_state: Initial state, "on" or "off" (optional).
        """
        self.id = id
        self.nodes = nodes
        self.source_name = source_name
        self.model_name = model_name
        self.initial_state = initial_state

    @property
    def spice_prefix(self):
        return "W"

    def __str__(self):
        parts = [f"{self.spice_prefix}{self.id}", " ".join(self.nodes), self.source_name, self.model_name]
        if self.initial_state:
            parts.append(self.initial_state)
        return " ".join(parts)
# >>>


# Class: LosslessTransmissionLine <<<
class LosslessTransmissionLine(Component):
    def __init__(
        self,
        id: str,
        nodes: tuple[str, str, str, str],
        impedance: str,
        td: str = "",
        frequency: str = "",
        nl: str = "0.25",
    ):
        """
        Spice lossless transmission line (T element).

        Args:
            id: Unique identifier for the transmission line.
            nodes: (n1+, n1-, n2+, n2-).
            impedance: Characteristic impedance Z0.
            td: Transmission delay (optional, specify either td or frequency).
            frequency: Frequency for NL-based delay specification (optional).
            nl: Normalized electrical length at frequency (default "0.25").
        """
        self.id = id
        self.nodes = nodes
        self.impedance = impedance
        self.td = td
        self.frequency = frequency
        self.nl = nl

    @property
    def spice_prefix(self):
        return "T"

    def __str__(self):
        parts = [f"{self.spice_prefix}{self.id}", " ".join(self.nodes), f"Z0={self.impedance}"]
        if self.td:
            parts.append(f"TD={self.td}")
        elif self.frequency:
            parts.append(f"F={self.frequency} NL={self.nl}")
        return " ".join(parts)
# >>>
