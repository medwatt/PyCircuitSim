# imports <<<
from pycircuitsim.simulator import NgSpiceSession, simulations
# >>>

# netlisting <<<
netlist = [
    "* Pole Zero Analysis Test",
    "V1 1 0 12 AC 1",
    "C1 1 2 1U",
    "C2 2 3 1U",
    "R3 2 0 1K",
    "R4 1 3 1K",
    ".end"
]
# >>>

# simulation <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Load the netlist into ngspice
session.load_netlist(netlist)

pz_simulation = simulations.PZ(
    nodes = ("1", "0", "3", "0"),
    source_type = "VOL",
    analysis_type = "PZ",
)

# Run simulation
session.run_simulation(pz_simulation)

# Get the data
data = session.get_all_data()

# Print the data
for k, v in data.data.items():
    print("")
    print(f"{k}: {v}")

# >>>
