# imports <<<
from __future__ import annotations
import copy
from .components.base import SubCircuitInstance
# >>>

class Circuit:

    # component methods <<<
    from .components.passive import R, L, C, K, S, W, T
    from .components.independent import (
        V, I,
        VoltagePulse, CurrentPulse,
        VoltageSin, CurrentSin,
        VoltageExp, CurrentExp,
        VoltagePWL, CurrentPWL,
        VoltageTransientNoise, CurrentTransientNoise,
    )
    from .components.dependent import G, E, F, H, B
    from .components.semiconductors import J, D, M, Q
    from .components.instance import X, N
    # >>>

    def __init__(self, title: str = "Default Circuit") -> None:
        self.title = title
        self.components = []
        self.subcircuits = {}
        self.includes = []
        self.param_defs = []
        self.models = []
        self.initial_conditions = []
        self.nodesets = []
        self.raw_spice_commands = []
        self.used_ids = {}

    # control <<<
    def include(self, path: str) -> None:
        self.includes.append(f'.include "{path}"')

    def lib(self, path: str, section: str | None = None) -> None:
        if section:
            self.includes.append(f'.lib "{path}" {section}')
        else:
            self.includes.append(f'.lib "{path}"')

    def param(self, **params) -> None:
        params_str = " ".join(f"{k}={v}" for k, v in params.items())
        self.param_defs.append(f".param {params_str}")

    def model(self, name: str, model_type: str, **params) -> None:
        params_str = " ".join(f"{k}={v}" for k, v in params.items())
        self.models.append(f".model {name} {model_type} ({params_str})")

    def ic(self, **node_conditions) -> None:
        conditions_str = " ".join(f"v({k})={v}" for k, v in node_conditions.items())
        self.initial_conditions.append(f".ic {conditions_str}")

    def nodeset(self, all_value: str = "", **node_guesses) -> None:
        if all_value:
            self.nodesets.append(f".nodeset all={all_value}")
        else:
            guesses_str = " ".join(f"v({k})={v}" for k, v in node_guesses.items())
            self.nodesets.append(f".nodeset {guesses_str}")

    def raw(self, line: str) -> None:
        self.raw_spice_commands.append(line)

    def va(self, id: str, nodes: tuple[str, ...], module: str, **params) -> None:
        """Add a VerilogA component instance.

        Creates an N-element instance and the corresponding ``.model``
        definition automatically.

        id: Unique identifier.
        nodes: Tuple of connecting nodes.
        module: VerilogA module name (as declared in the ``.va`` file).
        **params: Module parameter overrides.
        """
        model_name = f"{module}_{id}"
        self.N(id, nodes, model_name)
        self.model(model_name, module, **params)
    # >>>

    # build <<<
    def _check_id(self, prefix: str, id: str) -> None:
        if prefix not in self.used_ids:
            self.used_ids[prefix] = set()
        if id in self.used_ids[prefix]:
            raise ValueError(
                f"Identifier '{id}' is already used for component type '{prefix}'."
            )
        self.used_ids[prefix].add(id)

    def _add_component(self, component) -> None:
        self._check_id(component.spice_prefix, component.id)
        self.components.append(component)
        if isinstance(component, SubCircuitInstance):
            subckt = component.subcircuit
            if component.copy and isinstance(subckt, SubCircuit):
                subckt = subckt.copy(component.id)
            if isinstance(subckt, SubCircuit) and subckt.name not in self.subcircuits:
                self.subcircuits[subckt.name] = subckt
    # >>>

    # netlist <<<
    def _extend_lines(self, lines: list[str]) -> None:
        lines.extend(self.param_defs)
        lines.extend(self.models)
        for component in self.components:
            lines.append(str(component))
        lines.extend(self.raw_spice_commands)
        lines.extend(self.nodesets)
        lines.extend(self.initial_conditions)

    def get_netlist(self) -> list[str]:
        lines = [f"* {self.title}"]
        lines.extend(self.includes)
        for subckt in self.subcircuits.values():
            lines.extend(subckt.get_netlist())
        self._extend_lines(lines)
        lines.append(".end")
        return lines

    def __str__(self) -> str:
        return "\n".join(self.get_netlist())
    # >>>

class SubCircuit(Circuit):
    def __init__(
        self,
        name: str,
        nodes: list[str],
        params: dict[str, object] | None = None,
    ) -> None:
        super().__init__(title=name)
        self.name = name
        self.nodes = nodes
        self.params = params or {}

    def copy(self, id_suffix: str) -> SubCircuit:
        new = copy.deepcopy(self)
        new.name = f"{self.name}_{id_suffix}"
        return new

    def get_netlist(self) -> list[str]:
        params_str = " ".join(f"{k}={v}" for k, v in self.params.items())
        lines = [f'.subckt {self.name} {" ".join(self.nodes)} {params_str}'.strip()]
        self._extend_lines(lines)
        lines.append(f".ends {self.name}")
        for subckt in self.subcircuits.values():
            lines.extend(subckt.get_netlist())
        return lines

    def __str__(self) -> str:
        return "\n".join(self.get_netlist())
