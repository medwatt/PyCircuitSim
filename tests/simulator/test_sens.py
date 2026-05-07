# imports <<<
from pycircuitsim.simulator import NgSpiceSession, simulations
# >>>

# netlisting <<<
netlist = [
    "* Sensitivity Analysis Test",
    "V1 in 0 DC 1",
    "R1 in out 1k",
    "R2 out 0 1k",
    ".end"
]
# >>>

# simulation <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Load the netlist into ngspice
session.load_netlist(netlist)

sens_simulation = simulations.Sens(output_variable="V(out)")

# Run simulation
session.run_simulation(sens_simulation)

# Get the data
data = session.get_all_data()

# Print the data
for k, v in data.data.items():
    print("")
    print(f"{k}: {v}")

# >>>
