# imports <<<
from __future__ import annotations
from .base import Component, SubCircuitInstance
# >>>


def X(
    self,
    id: str,
    nodes: tuple[str, ...],
    subcircuit: object,
    params: dict[str, object] | None = None,
    copy: bool = False,
) -> None:
    """Add a subcircuit instance (X element).

    id: Unique identifier.
    nodes: Tuple of connecting nodes (must match the subcircuit's port order).
    subcircuit: SubCircuit definition object, or a string name for an externally defined subcircuit.
    params: Parameter overrides for parameterised subcircuits (optional).
    copy: If True, deep-copies the subcircuit definition and renames
        it ``<name>_<id>`` so each instance gets its own copy.
    """
    self._add_component(
        SubCircuitInstance(
            id=id, nodes=nodes, subcircuit=subcircuit, params=params, copy=copy
        )
    )


def N(self, id: str, nodes: tuple[str, ...], model: str, **params) -> None:
    """Add an OSDI model instance (N element).

    id: Unique identifier.
    nodes: Tuple of connecting nodes.
    model: OSDI model name.
    **params: Model parameter overrides.
    """
    params_str = " ".join(f"{k}={v}" for k, v in params.items())
    self._add_component(
        Component(
            id=id,
            spice_prefix="N",
            netlist_str=f"N{id} {' '.join(nodes)} {model} {params_str}".strip(),
        )
    )
