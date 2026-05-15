from __future__ import annotations

from .base import Component


def R(self, id: str, nodes: tuple[str, str], value: str, **params) -> None:
    """Add a resistor.

    id: Unique identifier.
    nodes: (plus_node, minus_node).
    value: Resistance value.
    **params: Additional SPICE parameters.
    """
    params_str = " ".join(f"{k}={v}" for k, v in params.items())
    self._add_component(Component(id=id, spice_prefix="R", netlist_str=f"R{id} {' '.join(nodes)} {value} {params_str}".strip()))


def L(self, id: str, nodes: tuple[str, str], value: str, **params) -> None:
    """Add an inductor.

    id: Unique identifier.
    nodes: (plus_node, minus_node).
    value: Inductance value.
    **params: Additional SPICE parameters.
    """
    params_str = " ".join(f"{k}={v}" for k, v in params.items())
    self._add_component(Component(id=id, spice_prefix="L", netlist_str=f"L{id} {' '.join(nodes)} {value} {params_str}".strip()))


def C(self, id: str, nodes: tuple[str, str], value: str, **params) -> None:
    """Add a capacitor.

    id: Unique identifier.
    nodes: (plus_node, minus_node).
    value: Capacitance value.
    **params: Additional SPICE parameters.
    """
    params_str = " ".join(f"{k}={v}" for k, v in params.items())
    self._add_component(Component(id=id, spice_prefix="C", netlist_str=f"C{id} {' '.join(nodes)} {value} {params_str}".strip()))


def K(self, id: str, inductor1: str, inductor2: str, coupling: str) -> None:
    """Add mutual inductance between two inductors.

    id: Unique identifier.
    inductor1: ID of the first inductor (without L prefix).
    inductor2: ID of the second inductor (without L prefix).
    coupling: Coupling coefficient (0 < k ≤ 1).
    """
    self._add_component(Component(id=id, spice_prefix="K", netlist_str=f"K{id} L{inductor1} L{inductor2} {coupling}"))


def S(self, id: str, nodes: tuple[str, str, str, str], model: str, initial_state: str = "") -> None:
    """Add a voltage-controlled switch.

    id: Unique identifier.
    nodes: (n+, n-, nc+, nc-).
    model: Switch model name.
    initial_state: Initial state — ``"on"`` or ``"off"`` (optional).
    """
    parts = [f"S{id}", " ".join(nodes), model]
    if initial_state:
        parts.append(initial_state)
    self._add_component(Component(id=id, spice_prefix="S", netlist_str=" ".join(parts)))


def W(self, id: str, nodes: tuple[str, str], source: str, model: str, initial_state: str = "") -> None:
    """Add a current-controlled switch.

    id: Unique identifier.
    nodes: (n+, n-).
    source: Name of the controlling voltage source.
    model: Switch model name.
    initial_state: Initial state — ``"on"`` or ``"off"`` (optional).
    """
    parts = [f"W{id}", " ".join(nodes), source, model]
    if initial_state:
        parts.append(initial_state)
    self._add_component(Component(id=id, spice_prefix="W", netlist_str=" ".join(parts)))


def T(
    self,
    id: str,
    nodes: tuple[str, str, str, str],
    impedance: str,
    td: str = "",
    frequency: str = "",
    nl: str = "0.25",
) -> None:
    """Add a lossless transmission line.

    id: Unique identifier.
    nodes: (n1+, n1-, n2+, n2-).
    impedance: Characteristic impedance Z0.
    td: Transmission delay (specify either td or frequency).
    frequency: Frequency for NL-based delay specification.
    nl: Normalised electrical length at frequency (default ``"0.25"``).
    """
    parts = [f"T{id}", " ".join(nodes), f"Z0={impedance}"]
    if td:
        parts.append(f"TD={td}")
    elif frequency:
        parts.append(f"F={frequency} NL={nl}")
    self._add_component(Component(id=id, spice_prefix="T", netlist_str=" ".join(parts)))
