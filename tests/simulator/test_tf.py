# imports <<<
from pycircuitsim.simulator import NgSpiceSession, simulations
# >>>

# netlisting <<<
netlist = [
    "* Transfer Function Analysis Test",
    "V1 n1 0 1",
    "R1 n2 n1 1k",
    "R2 0 n2 4k",
    "R3 n2 n3 2k",
    "R4 n4 n3 3k",
    "R5 0 n3 5k",
    "V2 n4 0 0",
    ".end",
]
# >>>

# simulation <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Load the netlist into ngspice
session.load_netlist(netlist)

# Transfer funciton analysis
tf_sim = simulations.TF(
    output_variable="V(n2)",
    input_source="V1",
)

# Run operating point analysis
session.run_simulation(tf_sim)

# Get the data
data = session.get_all_data()

# Print the data
for k, v in data.data.items():
    print("")
    print(f"{k}: {v}")

# >>>

