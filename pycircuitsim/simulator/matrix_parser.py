import numpy as np
import tempfile
from typing import Callable


class MatrixParser:
    def __init__(self, send_command: Callable[[str], None]):
        """
        Initializes the MatrixParser with a reference to a send_command function.

        Args:
            send_command (function): Send a command to ngspice.
        """
        self.send_command = send_command

    def get_matrix(self) -> np.ndarray:
        """
        Dumps and parses the left-hand-size matrix.
        """

        with tempfile.NamedTemporaryFile(mode="w+", delete=True) as matrix_file:
            # Dump the matrix data to a temporary file
            self.send_command(f"mdump {matrix_file.name}")

            # Parse the matrix file
            matrix_file.seek(0)  # Move to the start of the file
            lines = matrix_file.readlines()

            if "LU form" in lines[0]:
                lines = lines[1:]

            size, matrix_type = lines[1].split()

            size = int(size)

            # Initialize an empty matrix based on type
            if matrix_type == "real":
                m = np.zeros((size, size), dtype=float)
            elif matrix_type == "complex":
                m = np.zeros((size, size), dtype=complex)
            else:
                raise ValueError(f"Unsupported matrix type: {matrix_type}")

            # Populate the matrix with parsed values
            if matrix_type == "real":
                for line in lines[2:-1]:  # Ignore the last line
                    row, col, value = line.split()
                    row, col = int(row) - 1, int(col) - 1  # Convert to 0-based indexing
                    m[row, col] = float(value)
            else:
                for line in lines[2:-1]:  # Ignore the last line
                    row, col, real_part, imag_part = line.split()
                    row, col = int(row) - 1, int(col) - 1  # Convert to 0-based indexing
                    m[row, col] = complex(float(real_part), float(imag_part))

        return m

    def get_rhs(self) -> np.ndarray:
        """
        Dumps and parses the right-hand side (RHS) vector file.

        Returns:
            numpy.ndarray: The parsed RHS vector as a 1D numpy array.
        """
        with tempfile.NamedTemporaryFile(mode="w+", delete=True) as rhs_file:
            # Dump the RHS data to a temporary file
            self.send_command(f"mrdump {rhs_file.name}")

            # Parse the RHS file
            rhs_file.seek(0)  # Move to the start of the file
            lines = rhs_file.readlines()

            if "\t" not in lines[0]:  # real
                rhs = np.array([float(line.strip()) for line in lines])
            else:  # complex
                rhs = np.array(
                    [
                        complex(float(real), float(imag))
                        for line in lines
                        for real, imag in [line.strip().split("\t")]
                    ]
                )

        return rhs
