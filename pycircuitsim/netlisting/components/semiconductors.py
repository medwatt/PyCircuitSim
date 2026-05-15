# imports <<<
from __future__ import annotations
from .base import Component
# >>>


def J(
    self, id: str, nodes: tuple[str, str, str], model: str, area: str = "", **params
) -> None:
    """Add a junction field-effect transistor (J element).

    id: Unique identifier.
    nodes: (drain, gate, source).
    model: JFET model name.
    area: Area scaling factor (optional).
    **params: Additional SPICE parameters.
    """
    parts = [f"J{id}", " ".join(nodes), model]
    if area:
        parts.append(area)
    params_str = " ".join(f"{k}={v}" for k, v in params.items())
    if params_str:
        parts.append(params_str)
    self._add_component(Component(id=id, spice_prefix="J", netlist_str=" ".join(parts)))


def D(self, id: str, nodes: tuple[str, str], model: str, **params) -> None:
    """Add a diode (D element).

    id: Unique identifier.
    nodes: (anode, cathode).
    model: Diode model name.
    **params: Additional SPICE parameters.
    """
    params_str = " ".join(f"{k}={v}" for k, v in params.items())
    self._add_component(
        Component(
            id=id,
            spice_prefix="D",
            netlist_str=f"D{id} {' '.join(nodes)} {model} {params_str}".strip(),
        )
    )


def M(self, id: str, nodes: tuple[str, str, str, str], model: str, **params) -> None:
    """Add a MOSFET (M element).

    id: Unique identifier.
    nodes: (drain, gate, source, bulk).
    model: MOSFET model name.
    **params: Additional SPICE parameters (e.g. ``w``, ``l``).
    """
    params_str = " ".join(f"{k}={v}" for k, v in params.items())
    self._add_component(
        Component(
            id=id,
            spice_prefix="M",
            netlist_str=f"M{id} {' '.join(nodes)} {model} {params_str}".strip(),
        )
    )


def Q(
    self,
    id: str,
    nodes: tuple[str, str, str],
    model: str,
    ns: str = "",
    tj: str = "",
    **params,
) -> None:
    """Add a bipolar junction transistor (Q element).

    id: Unique identifier.
    nodes: (collector, base, emitter).
    model: BJT model name.
    ns: Noise factor (optional).
    tj: Junction temperature (optional).
    **params: Additional SPICE parameters.
    """
    parts = [f"Q{id}", " ".join(nodes)]
    if ns:
        parts.append(ns)
    if tj:
        parts.append(tj)
    parts.append(model)
    parts.extend(f"{k}={v}" for k, v in params.items())
    self._add_component(Component(id=id, spice_prefix="Q", netlist_str=" ".join(parts)))
