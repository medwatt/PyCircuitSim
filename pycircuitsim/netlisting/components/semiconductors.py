from .base import Component


# Class: JFET <<<
class JFET(Component):
    def __init__(self, id: str, nodes: tuple[str, str, str], model_name: str, area: str = "", **params):
        """
        Spice junction field-effect transistor (J element).

        Args:
            id: Unique identifier for the JFET.
            nodes: (drain, gate, source).
            model_name: Name of the JFET model.
            area: Area scaling factor (optional).
        """
        self.id = id
        self.nodes = nodes
        self.model_name = model_name
        self.area = area
        self.params = params

    @property
    def spice_prefix(self):
        return "J"

    def __str__(self):
        parts = [f"{self.spice_prefix}{self.id}", " ".join(self.nodes), self.model_name]
        if self.area:
            parts.append(self.area)
        params_str = " ".join(f"{k}={v}" for k, v in self.params.items())
        if params_str:
            parts.append(params_str)
        return " ".join(parts)
# >>>


# Class: Diode <<<
class Diode(Component):
    def __init__(self, id: str, nodes: tuple[str, str], model_name: str, **params):
        """
        Spice diode component.

        Args:
            id: Unique identifier for the diode.
            nodes: (anode, cathode).
            model_name: Name of the diode model.
        """
        self.id = id
        self.nodes = nodes
        self.model_name = model_name
        self.params = params

    @property
    def spice_prefix(self):
        return "D"

    def __str__(self):
        params_str = " ".join(f"{k}={v}" for k, v in self.params.items())
        return f'{self.spice_prefix}{self.id} {" ".join(self.nodes)} {self.model_name} {params_str}'.strip()
# >>>


# Class: Mosfet <<<
class Mosfet(Component):
    def __init__(self, id: str, nodes: tuple[str, str, str, str], model_name: str, **params):
        """
        Spice MOSFET component.

        Args:
            id: Unique identifier for the MOSFET.
            nodes: (drain, gate, source, bulk).
            model_name: Name of the MOSFET model.
        """
        self.id = id
        self.nodes = nodes
        self.model_name = model_name
        self.params = params

    @property
    def spice_prefix(self):
        return "M"

    def __str__(self):
        params_str = " ".join(f"{k}={v}" for k, v in self.params.items())
        return f'{self.spice_prefix}{self.id} {" ".join(self.nodes)} {self.model_name} {params_str}'.strip()
# >>>


# Class: BJT <<<
class BJT(Component):
    def __init__(self, id: str, nodes: tuple[str, str, str], model_name: str, ns: str = "", tj: str = "", **params):
        """
        Spice bipolar junction transistor (BJT) component.

        Args:
            id: Unique identifier for the BJT.
            nodes: (collector, base, emitter).
            model_name: Name of the BJT model.
            ns: Noise factor (optional).
            tj: Junction temperature (optional).
        """
        self.id = id
        self.nodes = nodes
        self.model_name = model_name
        self.ns = ns
        self.tj = tj
        self.params = params

    @property
    def spice_prefix(self):
        return "Q"

    def __str__(self) -> str:
        components = [
            f"{self.spice_prefix}{self.id}",
            " ".join(self.nodes),
            f"{self.ns}" if self.ns else None,
            f"{self.tj}" if self.tj else None,
            f"{self.model_name}",
            *[f"{key}={value}" for key, value in self.params.items()],
        ]
        return " ".join(filter(None, components))
# >>>
