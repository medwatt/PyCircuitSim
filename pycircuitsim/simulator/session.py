# imports <<<
import numpy as np
from typing import TypeVar, cast

from . import simulations
from .ngspice import NgSpiceLibrary
from .organizer import DataOrganizerFactory, DataOrganizer
from .veriloga_model import VerilogaModel
from .matrix_parser import MatrixParser
from .helpers import (
    str_to_bytes,
    bytes_to_str,
    list_to_c_char_array,
    c_char_array_to_list,
    extract_simulation_type,
)

T = TypeVar('T', bound=DataOrganizer)
# >>>

class NgSpiceSession:
    """
    Manages an ngspice simulation session.
    Provides methods to load netlists, send commands, retrieve data, and run simulations.
    """

    # init <<<
    def __init__(self, libpath=None):
        self.ngspice_lib = NgSpiceLibrary(libpath)
        self.veriloga_models = []
    # >>>

    # add veriloga models <<<
    def add_veriloga_model(self, veriloga_model: VerilogaModel):
        self.veriloga_models.append(veriloga_model)
    # >>>

    # load_netlist <<<
    def load_netlist(self, netlist: list[str] | str):
        """Load netlist into ngspice."""

        if isinstance(netlist, str):
            netlist = netlist.split("\n")

        # Load veriloga models before loading netlist
        self.load_veriloga_models()

        # Load the netlist
        c_netlist = list_to_c_char_array(netlist)
        result = self.ngspice_lib.ngSpice_Circ(c_netlist)
        if result != 0:
            raise RuntimeError("Failed to load netlist into ngspice.")
    # >>>

    # load veriloga models <<<
    def load_veriloga_models(self):
        """
        Load veriloga models into ngspice.
        This must be done before loading the netlist.
        """
        for model in self.veriloga_models:
            model.compile_model()
            self.send_command(f'osdi "{str(model)}"')
    # >>>

    # send command <<<
    def send_command(self, command: str) -> None:
        """Send a command to ngspice."""
        c_command = str_to_bytes(command)
        result = self.ngspice_lib.ngSpice_Command(c_command)
        if result != 0:
            raise RuntimeError(f"Command '{command}' failed.")
    # >>>

    # get methods <<<
    def get_current_plot_name(self) -> str:
        """Get the name of the current plot."""
        c_plot_name = self.ngspice_lib.ngSpice_CurPlot()
        return bytes_to_str(c_plot_name)

    def get_all_plot_names(self) -> list[str]:
        """Get the names of all plots."""
        c_plot_names = self.ngspice_lib.ngSpice_AllPlots()
        return c_char_array_to_list(c_plot_names)

    def get_vector_names(self, plot_name: None | str = None) -> list[str]:
        """Get the names of all vectors in a plot."""
        if plot_name is None:
            plot_name = self.get_current_plot_name()
        c_plot_name = str_to_bytes(plot_name)
        c_vector_names = self.ngspice_lib.ngSpice_AllVecs(c_plot_name)
        return c_char_array_to_list(c_vector_names)

    def get_data(self, vector_name: str) -> np.ndarray | None:
        """Retrieve data for a given vector."""
        c_vector_name = str_to_bytes(vector_name)
        info_struct_ptr = self.ngspice_lib.ngGet_Vec_Info(c_vector_name)
        if not info_struct_ptr:
            return None
        info_struct = info_struct_ptr.contents
        if bool(info_struct.v_realdata):
            return np.ctypeslib.as_array(
                info_struct.v_realdata, shape=(info_struct.v_length,)
            )
        elif bool(info_struct.v_compdata):
            return np.ctypeslib.as_array(
                info_struct.v_compdata, shape=(info_struct.v_length,)
            ).view("complex128")
        else:
            return None

    def get_all_data(self, plot_name: None | str = None) -> DataOrganizer:
        """Retrieve all data from a plot."""
        if plot_name is None:
            plot_name = self.get_current_plot_name()
        vector_names = self.get_vector_names(plot_name)
        simulation_type = extract_simulation_type(plot_name)
        data_organizer = DataOrganizerFactory.create_data_organizer(simulation_type)
        for vector_name in vector_names:
            data = self.get_data(vector_name)
            data_organizer.add_data(vector_name, data)
        return data_organizer

    def get_matrix(self):
        """Retrieve the simulation matrix and right-hand side vector."""
        self.matrix_parser = MatrixParser(self.send_command)
        m = self.matrix_parser.get_matrix()
        rhs = self.matrix_parser.get_rhs()
        vector_names = self.get_vector_names()[::-1]
        return (m, rhs), vector_names
    # >>>

    # run simulation <<<
    def run_simulation(self, simulation: simulations.Simulation[T]) -> T:
        """
        Execute a simulation strategy and return the organized results.
        """
        simulation.execute(self.send_command)
        return cast(T, self.get_all_data())
    # >>>
