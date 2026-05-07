from .base import Component


# Class: Linear Dependent Source <<<
class LinearDependentSource(Component):
    def __init__(self, id: str, nodes: tuple[str, str, str, str], value: str, multiplier: float | None = None):
        """
        Spice linear dependent source component.

        Args:
            id: Unique identifier for the source.
            nodes: (n_plus, n_minus, nc_plus, nc_minus).
            value: Gain or transconductance value.
            multiplier: Scaling factor (optional).
        """
        self.id = id
        self.nodes = nodes
        self.value = value
        self.multiplier = multiplier

    def __str__(self):
        parts = [f"{self.spice_prefix}{self.id}", " ".join(self.nodes), self.value]
        if self.multiplier:
            parts.append(str(self.multiplier))
        return " ".join(parts)


class VoltageControlledCurrentSource(LinearDependentSource):
    """Voltage-controlled current source (G element)."""
    @property
    def spice_prefix(self):
        return "G"


class VoltageControlledVoltageSource(LinearDependentSource):
    """Voltage-controlled voltage source (E element)."""
    @property
    def spice_prefix(self):
        return "E"


class CurrentControlledCurrentSource(LinearDependentSource):
    """Current-controlled current source (F element)."""
    @property
    def spice_prefix(self):
        return "F"


class CurrentControlledVoltageSource(LinearDependentSource):
    """Current-controlled voltage source (H element)."""
    @property
    def spice_prefix(self):
        return "H"
# >>>


# Class: Behavioral Source <<<
class BehavioralSource(Component):
    def __init__(self, id: str, nodes: tuple[str, str], current_expression: str = "", voltage_expression: str = ""):
        """
        Spice behavioral source (B element).

        Args:
            id: Unique identifier for the behavioral source.
            nodes: (positive_node, negative_node).
            current_expression: Expression defining current behavior (optional).
            voltage_expression: Expression defining voltage behavior (optional).

        Raises:
            ValueError: Exactly one of current_expression or voltage_expression must be specified.
        """
        if not (current_expression or voltage_expression):
            raise ValueError("A current or voltage expression must be defined.")
        if current_expression and voltage_expression:
            raise ValueError("Only one expression must be defined.")
        self.id = id
        self.nodes = nodes
        self.current_expression = current_expression
        self.voltage_expression = voltage_expression

    @property
    def spice_prefix(self):
        return "B"

    def __str__(self):
        expression = f"i={self.current_expression}" if self.current_expression else f"v={self.voltage_expression}"
        return f"{self.spice_prefix}{self.id} {' '.join(self.nodes)} {expression}"
# >>>
