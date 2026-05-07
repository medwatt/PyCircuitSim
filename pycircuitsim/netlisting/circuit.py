# imports <<<
import copy
from .circuit_components import CircuitComponents
from .circuit_methods import CircuitMethods
from .components.instance import SubCircuitInstance
# >>>

# Class: Circuit <<<
class Circuit(CircuitComponents, CircuitMethods):
    def __init__(self, title="Default Circuit"):
        self.title = title
        self.components = []
        self.subcircuits = {}
        self.includes = []
        self.param_defs = []
        self.models = []
        self.raw_spice_commands = []
        self.initial_conditions = []
        self.nodesets = []
        self.used_ids = {}

    # Add components to netlist <<<
    def _check_id(self, prefix, id) -> None:
        if prefix not in self.used_ids:
            self.used_ids[prefix] = set()
        if id in self.used_ids[prefix]:
            raise ValueError(
                f"Identifier '{id}' is already used for component type '{prefix}'."
            )
        self.used_ids[prefix].add(id)

    def _add_component(self, component) -> None:
        prefix = component.spice_prefix
        self._check_id(prefix, component.id)
        self.components.append(component)
        if isinstance(component, SubCircuitInstance):
            subckt = component.subcircuit
            if component.copy:
                subckt = subckt.copy(component.id)
            if subckt.name not in self.subcircuits:
                self.subcircuits[subckt.name] = subckt
    # >>>

    # Build netlist <<<
    def _extend_lines(self, lines) -> None:
        lines.extend(self.param_defs)
        lines.extend(self.models)
        for component in self.components:
            lines.append(str(component))
        lines.extend(self.raw_spice_commands)
        lines.extend(self.nodesets)
        lines.extend(self.initial_conditions)

    def get_netlist(self) -> list:
        lines = [f"* {self.title}"]
        lines.extend(self.includes)
        for subckt in self.subcircuits.values():
            lines.extend(subckt.get_netlist())
        self._extend_lines(lines)
        lines.extend([".end"])
        return lines

    def __str__(self) -> str:
        return "\n".join(self.get_netlist())
    # >>>
# >>>

# Class: SubCircuit <<<
class SubCircuit(Circuit):
    def __init__(self, name: str, nodes: list, params: dict = {}):
        super().__init__(title=name)
        self.name = name
        self.nodes = nodes
        self.params = params or {}

    def copy(self, id_suffix):
        new_subcircuit = copy.deepcopy(self)
        new_subcircuit.name = f"{self.name}_{id_suffix}"
        return new_subcircuit

    def get_netlist(self) -> list:
        params_str = " ".join(f"{k}={v}" for k, v in self.params.items())
        lines = [f'.subckt {self.name} {" ".join(self.nodes)} {params_str}'.strip()]
        super()._extend_lines(lines)
        lines.append(f".ends {self.name}")
        for subckt in self.subcircuits.values():
            lines.extend(subckt.get_netlist())
        return lines

    def __str__(self) -> str:
        return "\n".join(self.get_netlist())
# >>>
