# imports <<<
from pycircuitsim.simulator import NgSpiceSession, simulations
# >>>

# netlisting <<<
netlist = [
    "* Transient Analysis Test",
    "V1 in 0 PULSE(0 10 0.0 0.0 0.0 0.0 0.0025)",
    "R1 in n1 1k",
    "C1 n1 0 1u",
    ".end"
]
# >>>

# simulation <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Load the netlist into ngspice
session.load_netlist(netlist)

tran_simulation = simulations.Tran(
    tstep = 1e-4,
    tstop = 5e-3,
)

# Run simulation
session.run(tran_simulation)

# Get the data
data = session.get_all_data()

# Print the data
for k, v in data.data.items():
    print("")
    print(f"{k}: {v}")

# >>>>
