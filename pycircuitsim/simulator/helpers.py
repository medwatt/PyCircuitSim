import re
from ctypes import c_char_p, Array

# normalize spice text <<<
_PATH_DIRECTIVES = frozenset({".include", ".inc", ".lib", "osdi", ".hdl"})


def normalize_spice_line(line: str) -> str:
    """Lowercase a single SPICE line, preserving paths after path-bearing
    directives (.include/.inc/.lib/osdi/.hdl). Comment lines pass through."""
    stripped = line.lstrip()
    if not stripped or stripped[0] == "*":
        return line
    first = stripped.split(None, 1)[0]
    if first.lower() in _PATH_DIRECTIVES:
        i = line.index(first)
        return line[:i] + first.lower() + line[i + len(first):]
    return line.lower()


def normalize_spice_text(text: str) -> str:
    """Lowercase a SPICE netlist line by line, preserving paths."""
    return "\n".join(normalize_spice_line(ln) for ln in text.splitlines())
# >>>

# string to bytes <<<
def str_to_bytes(string: str) -> bytes:
    """Convert a Python string to bytes, normalizing SPICE case."""
    return normalize_spice_text(string).encode("utf-8")
# >>>

# bytes to string <<<
def bytes_to_str(bstring: bytes) -> str:
    """Convert bytes to a Python string."""
    return bstring.decode("utf-8")
# >>>

# list of strings to c char array <<<
def list_to_c_char_array(lst: list[str]) -> Array[c_char_p]:
    """Convert a Python list of strings to a C array of c_char_p."""
    # Create a list of c_char_p from the Python list of strings
    char_array = (c_char_p * (len(lst) + 1))()

    # Assign the Python strings (as bytes) to the array
    for i, string in enumerate(lst):
        char_array[i] = str_to_bytes(string)

    # Set the last element to None (null pointer) to terminate the array
    char_array[len(lst)] = None

    return char_array
# >>>

# c char array to list of strings <<<
def c_char_array_to_list(charpp: Array[c_char_p]) -> list[str]:
    """Convert a C array of c_char_p to a Python list of strings."""
    result = []
    i = 0
    # Loop through the char** until a null pointer is found
    while charpp[i] is not None:
        # Get the string from the current pointer
        result.append(charpp[i].decode("utf-8"))
        i += 1
    return result
# >>>

def extract_simulation_type(plot_name: str) -> str:
    """Extract the simulation type from plot name."""
    match = re.match(r'([a-zA-Z]+)', plot_name)
    if match:
        return match.group(1)
    else:
        return 'unknown'
