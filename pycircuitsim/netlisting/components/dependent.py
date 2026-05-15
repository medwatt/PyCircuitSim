from __future__ import annotations

from .base import Component


def G(self, id: str, nodes: tuple[str, str, str, str], value: str, multiplier: float | None = None) -> None:
    """Add a voltage-controlled current source (G element).

    id: Unique identifier.
    nodes: (n+, n-, nc+, nc-).
    value: Transconductance value.
    multiplier: Scaling factor (optional).
    """
    parts = [f"G{id}", " ".join(nodes), value]
    if multiplier is not None:
        parts.append(str(multiplier))
    self._add_component(Component(id=id, spice_prefix="G", netlist_str=" ".join(parts)))


def E(self, id: str, nodes: tuple[str, str, str, str], value: str, multiplier: float | None = None) -> None:
    """Add a voltage-controlled voltage source (E element).

    id: Unique identifier.
    nodes: (n+, n-, nc+, nc-).
    value: Voltage gain.
    multiplier: Scaling factor (optional).
    """
    parts = [f"E{id}", " ".join(nodes), value]
    if multiplier is not None:
        parts.append(str(multiplier))
    self._add_component(Component(id=id, spice_prefix="E", netlist_str=" ".join(parts)))


def F(self, id: str, nodes: tuple[str, str, str, str], value: str, multiplier: float | None = None) -> None:
    """Add a current-controlled current source (F element).

    id: Unique identifier.
    nodes: (n+, n-, nc+, nc-).
    value: Current gain.
    multiplier: Scaling factor (optional).
    """
    parts = [f"F{id}", " ".join(nodes), value]
    if multiplier is not None:
        parts.append(str(multiplier))
    self._add_component(Component(id=id, spice_prefix="F", netlist_str=" ".join(parts)))


def H(self, id: str, nodes: tuple[str, str, str, str], value: str, multiplier: float | None = None) -> None:
    """Add a current-controlled voltage source (H element).

    id: Unique identifier.
    nodes: (n+, n-, nc+, nc-).
    value: Transresistance value.
    multiplier: Scaling factor (optional).
    """
    parts = [f"H{id}", " ".join(nodes), value]
    if multiplier is not None:
        parts.append(str(multiplier))
    self._add_component(Component(id=id, spice_prefix="H", netlist_str=" ".join(parts)))


def B(
    self,
    id: str,
    nodes: tuple[str, str],
    *,
    current_expression: str = "",
    voltage_expression: str = "",
) -> None:
    """Add a behavioral source (B element).

    Provide exactly one of ``current_expression`` or ``voltage_expression``.

    id: Unique identifier.
    nodes: (positive_node, negative_node).
    current_expression: Expression defining current behaviour (optional).
    voltage_expression: Expression defining voltage behaviour (optional).

    Raises:
        ValueError: If neither or both expressions are provided.
    """
    if not (current_expression or voltage_expression):
        raise ValueError("A current or voltage expression must be defined.")
    if current_expression and voltage_expression:
        raise ValueError("Only one expression must be defined.")
    expression = f"i={current_expression}" if current_expression else f"v={voltage_expression}"
    self._add_component(Component(id=id, spice_prefix="B", netlist_str=f"B{id} {' '.join(nodes)} {expression}"))
