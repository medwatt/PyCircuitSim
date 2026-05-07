from ..simulator import VerilogaModel

# helper function <<<
def dict_to_str(d: dict) -> str:
    return " ".join(f"{k}={v}" for k, v in d.items())

def nodes_to_voltage_string(d: dict) -> str:
    return " ".join(f"v({k})={v}" for k, v in d.items())
# >>>

class CircuitMethods:

    # include <<<
    def include(self, path: str) -> None:
        """Add a .include directive to load an external SPICE file."""
        self.includes.append(f'.include "{path}"')

    def lib(self, path: str, section: str | None = None) -> None:
        """Add a .lib directive to load a model library or a specific section of one."""
        if section:
            self.includes.append(f'.lib "{path}" {section}')
        else:
            self.includes.append(f'.lib "{path}"')
    # >>>

    # param <<<
    def param(self, **params) -> None:
        """Define one or more .param variables."""
        params_str = " ".join(f"{k}={v}" for k, v in params.items())
        self.param_defs.append(f".param {params_str}")
    # >>>

    # define model <<<
    def define_model(self, model_name: str, model_type: str, **params) -> None:
        """Define a SPICE model."""
        self.models.append(f".model {model_name} {model_type} ({dict_to_str(params)})")
    # >>>

    # add raw spice <<<
    def add_raw_spice(self, command: str) -> None:
        """Add a raw SPICE command to the circuit."""
        self.raw_spice_commands.append(command)
    # >>>

    # set initial conditions <<<
    def set_initial_conditions(self, node_conditions: dict) -> None:
        """
        Set initial conditions for nodes in the transient analysis.

        Args:
            node_conditions: Dictionary where keys are node names and values are the desired initial voltages.
        """
        self.initial_conditions.append(f".ic {nodes_to_voltage_string(node_conditions)}")
    # >>>

    # set nodeset <<<
    def set_nodeset(self, all_value: str = "", node_guesses: dict = {}) -> None:
        """
        Specify initial guesses for node voltages to aid DC convergence.

        Args:
            all_value: If provided, sets all nodes (except ground) to this initial voltage guess.
            node_guesses: Dictionary where keys are node names and values are initial guesses for their voltages.
        """
        if all_value:
            nodeset_str = f".nodeset all={all_value}"
        else:
            nodeset_str = f".nodeset {nodes_to_voltage_string(node_guesses)}"
        self.nodesets.append(nodeset_str)
    # >>>

    # veriloga <<<
    def veriloga(self, id: str, nodes: tuple[str, ...], veriloga_model: VerilogaModel, params: dict = {}) -> None:
        """
        Add a VerilogA component instance.

        Args:
            id: Unique identifier for the instance.
            nodes: Tuple of nodes connecting to the component.
            veriloga_model: The VerilogA model to instantiate.
            params: Dictionary of parameter values (optional).
        """
        model_type = veriloga_model.module_name
        model_name = f"{model_type}_{id}"
        self.components.append(f"N{id} {' '.join(nodes)} {model_name}")
        self.define_model(model_name, model_type, **params)
    # >>>
