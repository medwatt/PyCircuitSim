# imports <<<
from pycircuitsim.simulator import NgSpiceSession, simulations
# >>>

# netlisting <<<
netlist = [
    "* AC Analysis Test",
    "V1 in 0 1 AC 1",
    "R1 in out 1k",
    "C1 out 0 1u",
    ".end"
]
# >>>

# simulation <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Load the netlist into ngspice
session.load_netlist(netlist)

# Initialize a AC simulation object
ac_sim = simulations.AC(
    sweep_type = "dec",
    points = 10,
    fstart = 1,
    fstop = 1e6,
)


# Run simulation
session.run_simulation(ac_sim)

# Get matrix
(m, rhs), vector_names = session.get_matrix()

print(m)
print("")
print(rhs)

# >>>
