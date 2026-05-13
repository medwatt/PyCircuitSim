from abc import ABC, abstractmethod
from typing import Generic, TypeVar, TYPE_CHECKING, cast

from .organizer import (
    DataOrganizer,
    OpDataOrganizer,
    TranDataOrganizer,
    AcDataOrganizer,
    TfDataOrganizer,
    PzDataOrganizer,
    SensDataOrganizer,
    FourDataOrganizer,
    DefaultDataOrganizer,
)

if TYPE_CHECKING:
    from .session import NgSpiceSession

R = TypeVar("R")
T = TypeVar("T", bound=DataOrganizer)


# runnable <<<
class Runnable(ABC, Generic[R]):
    """Anything that can be executed by an NgSpiceSession via session.run(...)."""

    @abstractmethod
    def execute(self, session: "NgSpiceSession") -> R:
        pass
# >>>


# abstract class <<<
class Simulation(Runnable[T]):
    """
    Abstract base class for single-command simulations.
    """

    @abstractmethod
    def build_command(self) -> str:
        pass

    def execute(self, session: "NgSpiceSession") -> T:
        session.send_command(self.build_command())
        return cast(T, session.get_all_data())

    def __str__(self) -> str:
        return self.build_command()
# >>>


# operating point <<<
class OP(Simulation[OpDataOrganizer]):
    """
    Operating Point simulation.
    """

    def build_command(self):
        return "op"
# >>>


# dc <<<
class DC(Simulation[OpDataOrganizer]):
    """
    DC Sweep simulation.
    """

    def __init__(
        self,
        src1: tuple[str, float, float, float],
        src2: tuple[str, float, float, float] | None = None,
    ):
        self.src1 = src1
        self.src2 = src2

    def build_command(self):
        # Construct the command for the first source
        command = f"dc {self.src1[0]} {self.src1[1]} {self.src1[2]} {self.src1[3]}"
        # If a second source is provided, append its parameters
        if self.src2:
            command += f" {self.src2[0]} {self.src2[1]} {self.src2[2]} {self.src2[3]}"
        return command
# >>>


# ac <<<
class AC(Simulation[AcDataOrganizer]):
    """
    AC simulation.
    """

    def __init__(self, sweep_type: str, points: int, fstart: float, fstop: float):
        if sweep_type not in {"dec", "lin", "oct"}:
            raise ValueError("Invalid sweep type. Must be 'dec', 'lin', or 'oct'.")
        self.sweep_type = sweep_type
        self.points = points
        self.fstart = fstart
        self.fstop = fstop

    def build_command(self):
        command = f"ac {self.sweep_type} {self.points} {self.fstart} {self.fstop}"
        return command
# >>>


# transient <<<
class Tran(Simulation[TranDataOrganizer]):
    """
    Transient simulation.
    """

    def __init__(
        self,
        tstep: float,
        tstop: float,
        tstart: float | None = None,
        tmax: float | None = None,
        uic: bool = False,
    ):
        if tmax is not None and tstart is None:
            raise ValueError("If tmax is provided, tstart must also be provided.")
        self.tstep = tstep
        self.tstop = tstop
        self.tstart = tstart
        self.tmax = tmax
        self.uic = uic

    def build_command(self):
        params = [self.tstep, self.tstop, self.tstart, self.tmax]
        params = [str(p) for p in params if p is not None]
        if self.uic:
            params.append("uic")
        command = "tran " + " ".join(params)
        return command
# >>>


# transfer function <<<
class TF(Simulation[TfDataOrganizer]):
    """
    Transfer Function analysis.
    """

    def __init__(self, output_variable: str, input_source: str):
        """

        Args:
            output_variable: The small signal output variable.
            input_source: The the small-signal input source.
        """
        self.output_variable = output_variable
        self.input_source = input_source

    def build_command(self):
        command = f"tf {self.output_variable} {self.input_source}"
        return command
# >>>


# pole zero <<<
class PZ(Simulation[PzDataOrganizer]):
    """
    Pole-Zero analysis.
    """

    def __init__(
        self, nodes: tuple[str, str, str, str], source_type: str, analysis_type: str
    ):
        """
        Initializes a Pole-Zero analysis command.

        Args:
            nodes: A tuple of four nodes (node1, node2, node3, node4)
            source_type: Source type ("cur" for current or "vol" for voltage)
            analysis_type: Analysis type ("pol" for pole, "zer" for zero, or "pz" for both)
        """
        self.nodes = nodes
        self.source_type = source_type.lower()
        self.analysis_type = analysis_type.lower()

        if len(self.nodes) != 4:
            raise ValueError("Exactly four nodes must be provided.")
        if self.source_type not in {"cur", "vol"}:
            raise ValueError('Invalid source type. Must be "cur" or "vol".')
        if self.analysis_type not in {"pol", "zer", "pz"}:
            raise ValueError('Invalid analysis type. Must be "pol", "zer", or "pz".')

    def build_command(self):
        node_str = " ".join(self.nodes)
        command = f"pz {node_str} {self.source_type} {self.analysis_type}"
        return command
# >>>


# sensitivity <<<
class Sens(Simulation[SensDataOrganizer]):
    """
    DC Sensitivity analysis.
    """

    def __init__(self, output_variable: str):
        """
        Args:
            output_variable: The output variable to compute sensitivities for (e.g. "V(out)").
        """
        self.output_variable = output_variable

    def build_command(self):
        return f"sens {self.output_variable}"
# >>>


# fourier <<<
class Four(Simulation[FourDataOrganizer]):
    """
    Fourier analysis. Must be run after a transient simulation.
    """

    def __init__(
        self,
        freq: float,
        output_variables: list[str] | str,
        n_harmonics: int | None = None,
    ):
        """
        Args:
            freq: Fundamental frequency for the Fourier analysis.
            output_variables: One or more output variables to analyze.
            n_harmonics: Number of harmonics to compute (default: 9).
        """
        if isinstance(output_variables, str):
            output_variables = [output_variables]
        self.freq = freq
        self.output_variables = output_variables
        self.n_harmonics = n_harmonics

    def build_command(self):
        parts = ["fourier", str(self.freq)]
        if self.n_harmonics is not None:
            parts.append(str(self.n_harmonics))
        parts.extend(self.output_variables)
        return " ".join(parts)
# >>>


# noise <<<
class Noise(Simulation[DefaultDataOrganizer]):
    """
    AC Noise analysis.
    """

    def __init__(
        self,
        output: str,
        src: str,
        sweep_type: str,
        points: int,
        fstart: float,
        fstop: float,
        pts_per_summary: int | None = None,
    ):
        """
        Initializes a Noise analysis command.

        Args:
            output: The node at which the total output noise is desired.
            src: The independent source to which input noise is referred.
            sweep_type: Type of frequency sweep ("dec", "lin", or "oct").
            points: Number of points in the sweep.
            fstart: Start frequency.
            fstop: Stop frequency.
            pts_per_summary: Optional integer specifying points per summary.
        """
        if sweep_type not in {"dec", "lin", "oct"}:
            raise ValueError('Invalid sweep type. Must be "dec", "lin", or "oct".')

        self.output = output
        self.src = src
        self.sweep_type = sweep_type
        self.points = points
        self.fstart = fstart
        self.fstop = fstop
        self.pts_per_summary = pts_per_summary

    def build_command(self):
        command = f"noise {self.output} {self.src} {self.sweep_type} {self.points} {self.fstart} {self.fstop}"
        if self.pts_per_summary is not None:
            command += f" {self.pts_per_summary}"
        return command
# >>>


# parametric sweep <<<
class ParametricSweep(Runnable[dict]):
    """Runs a simulation repeatedly while sweeping a single component value."""

    def __init__(self, component: str, values: list, simulation: Simulation):
        """
        Args:
            component: Component to alter. Either a simple name (e.g. "R1") or
                       a full ngspice alter expression for hierarchical instances
                       (e.g. "@r.xtop.xsub.r1[resistance]").
            values: Sequence of values to sweep over.
            simulation: Simulation instance to run at each step.
        """
        self.component = component
        self.values = values
        self.simulation = simulation

    def execute(self, session: "NgSpiceSession") -> dict:
        results = {}
        for value in self.values:
            session.send_command(f"alter {self.component} {value}")
            results[value] = self.simulation.execute(session)
        return results
# >>>


# corner analysis <<<
class CornerAnalysis(Runnable[dict]):
    """Runs a simulation across a set of named parameter corners."""

    def __init__(self, corners: dict[str, dict], simulation: Simulation):
        """
        Args:
            corners: Mapping of corner name to a dict of {component: value}.
            simulation: Simulation instance to run at each corner.
        """
        self.corners = corners
        self.simulation = simulation

    def execute(self, session: "NgSpiceSession") -> dict:
        results = {}
        for name, params in self.corners.items():
            for component, value in params.items():
                session.send_command(f"alter {component} {value}")
            results[name] = self.simulation.execute(session)
        return results
# >>>
