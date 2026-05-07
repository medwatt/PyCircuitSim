# imports <<<
import os
from ctypes import util, cdll, c_char_p, c_int, POINTER, py_object, cast, byref, c_void_p

from .structs import vector_info
from .callbacks import NgSpiceCallbacks
from .message_handlers import StderrHandler, StdoutHandler, StatusHandler
# >>>


class NgSpiceLibrary:
    """
    Handles loading and initializing the ngspice shared library.
    """

    def __init__(self, libpath=None):
        self.libngspice = self._load_library(libpath or self._locate_ngspice())
        self._initialize_callbacks()
        self._initialize_api()

    def _initialize_callbacks(self):
        self.callbacks = NgSpiceCallbacks()
        self.callbacks.register_handler(StderrHandler())
        self.callbacks.register_handler(StdoutHandler())
        self.callbacks.register_handler(StatusHandler())

    def _locate_ngspice(self):
        libpath = util.find_library("ngspice")
        if libpath is None:
            raise FileNotFoundError("The ngspice shared library could not be found.")
        return libpath

    def _load_library(self, libpath):
       if os.path.isfile(libpath) or libpath:
           return cdll.LoadLibrary(libpath)
       raise FileNotFoundError(f"Shared library {libpath} not found")

    def _initialize_api(self):

        # Optional: Pass a Python object (like self) as a void* to the
        # C code and retrieve it back in the callbacks
        self._user_data = py_object(self) # Ensure that the object is not garbage collected

        """Initialize ngspice shared library functions."""
        self.libngspice.ngSpice_Init(
            self.callbacks.SendChar,
            self.callbacks.SendStat,
            self.callbacks.ControlledExit,
            self.callbacks.SendData,
            self.callbacks.SendInitData,
            self.callbacks.BGThreadRunning,
            cast(byref(self._user_data), c_void_p)
        )

        # Send circuit to ngspice
        self.libngspice.ngSpice_Circ.argtypes = [POINTER(c_char_p)]
        self.libngspice.ngSpice_Circ.restype = c_int

        # Send command to ngspice
        self.libngspice.ngSpice_Command.argtypes = [c_char_p]
        self.libngspice.ngSpice_Command.restype = c_int

        # Check if the ngspice simulation is currently running.
        self.libngspice.ngSpice_running.restype = c_int

        # Fetch vector information from ngspice by specifying vector name.
        self.libngspice.ngGet_Vec_Info.argtypes = [c_char_p]
        self.libngspice.ngGet_Vec_Info.restype = POINTER(vector_info)

        # Set up retrieval of all vector names in a specified plot, useful for analyzing simulation results.
        self.libngspice.ngSpice_AllVecs.argtypes = [c_char_p]
        self.libngspice.ngSpice_AllVecs.restype = POINTER(c_char_p)

        # Get the current active plot's name.
        self.libngspice.ngSpice_CurPlot.restype = c_char_p

        # Fetch all plot names created so far.
        self.libngspice.ngSpice_AllPlots.restype = POINTER(c_char_p)

    # >>>

    # ngspice api method <<<
    def ngSpice_Circ(self, circ_lines):
        """Wrapper for ngSpice_Circ function."""
        return self.libngspice.ngSpice_Circ(circ_lines)

    def ngSpice_Command(self, command):
        """Wrapper for ngSpice_Command function."""
        return self.libngspice.ngSpice_Command(command)

    def ngSpice_running(self):
        """Wrapper for ngSpice_running function."""
        return self.libngspice.ngSpice_running()

    def ngGet_Vec_Info(self, vector_name):
        """Wrapper for ngGet_Vec_Info function."""
        return self.libngspice.ngGet_Vec_Info(vector_name)

    def ngSpice_AllVecs(self, plot_name):
        """Wrapper for ngSpice_AllVecs function."""
        return self.libngspice.ngSpice_AllVecs(plot_name)

    def ngSpice_CurPlot(self):
        """Wrapper for ngSpice_CurPlot function."""
        return self.libngspice.ngSpice_CurPlot()

    def ngSpice_AllPlots(self):
        """Wrapper for ngSpice_AllPlots function."""
        return self.libngspice.ngSpice_AllPlots()
    # >>>
