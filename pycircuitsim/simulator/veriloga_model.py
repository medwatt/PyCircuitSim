import os
import subprocess
import shutil

class VerilogaModel:
    def __init__(self, module_name: str, path: str, always_recompile: bool = False):
        self.module_name = module_name
        self.path = path
        self.always_recompile = always_recompile

    def __str__(self) -> str:
        """Return the path of the compiled Veriloga model"""
        # Remove .va extension if present
        path_without_extension = os.path.splitext(self.path)[0]
        return f"{path_without_extension}.osdi"

    def compile_model(self):
        # Check if openvaf is installed
        if not shutil.which("openvaf"):
            raise EnvironmentError("openvaf is not installed or not in PATH.")

        # Check if osdi file exists and if compilation is necessary
        if not os.path.isfile(str(self)) or self.always_recompile:
            # Compile the Verilog-A model
            subprocess.run(["openvaf", self.path], check=True)


