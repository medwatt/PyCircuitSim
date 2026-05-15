from dataclasses import dataclass


@dataclass(slots=True)
class Component:
    id: str
    spice_prefix: str
    netlist_str: str

    def __str__(self) -> str:
        return self.netlist_str


class SubCircuitInstance:
    """SPICE subcircuit instance (X element). """

    def __init__(
        self,
        id: str,
        nodes: tuple[str, ...],
        subcircuit: object,
        params: dict[str, object] | None = None,
        copy: bool = False,
    ) -> None:
        self.id = id
        self.nodes = nodes
        self.subcircuit = subcircuit
        self.params = params or {}
        self.copy = copy

    @property
    def spice_prefix(self) -> str:
        return "X"

    def __str__(self) -> str:
        subckt_name = getattr(self.subcircuit, "name", str(self.subcircuit))
        if self.copy:
            subckt_name = f"{subckt_name}_{self.id}"
        params_str = " ".join(f"{k}={v}" for k, v in self.params.items())
        parts = [f"X{self.id}", " ".join(self.nodes), subckt_name]
        if params_str:
            parts.append(params_str)
        return " ".join(parts)
