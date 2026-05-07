from .simulations import Simulation


class ParametricSweep:
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

    def run(self, session) -> dict:
        """Run the sweep and return results keyed by swept value."""
        results = {}
        for value in self.values:
            session.send_command(f"alter {self.component} {value}")
            session.run_simulation(self.simulation)
            results[value] = session.get_all_data()
        return results
