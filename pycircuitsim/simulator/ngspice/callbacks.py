from ctypes import CFUNCTYPE, c_int, c_char_p, c_void_p, c_bool
from .message_handlers import MessageHandler
import threading

class NgSpiceCallbacks:
    """Handles ngspice callback functions."""

    def __init__(self):
        self._initialize_callbacks()
        self._handlers: list[MessageHandler] = []
        self._lock = threading.Lock()

    def register_handler(self, handler: MessageHandler) -> None:
        """Register a handler."""
        with self._lock:
            self._handlers.append(handler)

    def _notify_handlers(self, msg_type: str, message: str) -> None:
        """Notify all handlers."""
        with self._lock:
            for handler in self._handlers:
                handler.handle(msg_type, message)

    def _initialize_callbacks(self):
        """
        Set callback functions for ngspice.
        """

        @CFUNCTYPE(c_int, c_char_p, c_int, c_void_p)
        def SendChar(output: bytes, lib_id: int, ret_ptr: c_void_p) -> int:
            """
            Callback function for reading printf, fprintf, fputs from ngspice.

            Args:
                output:  output string from ngspice.
                lib_id:  identification number of calling ngspice shared lib.
                ret_ptr: return pointer received from caller
            """
            message = output.decode('utf-8').strip()
            # Determine message type based on prefixes
            if message.startswith('stdout'):
                msg_type = 'stdout'
                content = message[len('stdout'):].strip()
            elif message.startswith('stderr'):
                msg_type = 'stderr'
                content = message[len('stderr'):].strip()
            else:
                msg_type = 'stdout'  # Default to stdout
                content = message

            self._notify_handlers(msg_type, content)
            return 0

        @CFUNCTYPE(c_int, c_char_p, c_int, c_void_p)
        def SendStat(sim_stat: bytes, lib_id: int, ret_ptr: c_void_p) -> int:
            """
            Callback function for sending simulation status to caller.

            Args:
                output:  output string from ngspice.
                lib_id:  identification number of calling ngspice shared lib.
                ret_ptr: return pointer received from caller
            """
            status = sim_stat.decode('utf-8').strip()
            self._notify_handlers('status', status)
            return 0

        @CFUNCTYPE(c_int, c_int, c_bool, c_bool, c_int, c_void_p)
        def ControlledExit(exit_status: int, is_unload: c_bool, is_quit: c_bool, lib_id: int, ret_ptr: c_void_p) -> int:
            """
            Callback function for transferring a signal upon ngspice controlled exit to caller.
            """
            reason = 'quit' if is_quit else 'error'
            message = f'Exit Status: {exit_status}, Reason: {reason}, Unload: {bool(is_unload)}'
            self._notify_handlers('exit', message)
            return 0

        @CFUNCTYPE(c_int, c_void_p, c_int, c_int, c_void_p)
        def SendData(vecvaluesall_ptr, num_structs: int, lib_id: int, ret_ptr: c_void_p) -> int:
            """
            Callback function for sending data values of all vectors in the current plot.
            """
            self._notify_handlers('data', f'Data with {num_structs} structs received.')
            return 0

        @CFUNCTYPE(c_int, c_void_p, c_int, c_void_p)
        def SendInitData(vecinfoall_ptr, lib_id: int, ret_ptr: c_void_p) -> int:
            """
            Callback function for sending info on all vectors in the current plot before simulation starts.
            """
            self._notify_handlers('init_data', 'Initialization data received.')
            return 0

        @CFUNCTYPE(c_int, c_bool, c_int, c_void_p)
        def BGThreadRunning(is_running: c_bool, lib_id: int, ret_ptr: c_void_p) -> int:
            """
            Callback function for sending the background thread running status.
            """
            status = 'running' if is_running else 'not running'
            self._notify_handlers('bg_thread', f'Background thread is {status}.')
            return 0

        # Assign functions to instance variables
        self.SendChar = SendChar
        self.SendStat = SendStat
        self.ControlledExit = ControlledExit
        self.SendData = SendData
        self.SendInitData = SendInitData
        self.BGThreadRunning = BGThreadRunning
