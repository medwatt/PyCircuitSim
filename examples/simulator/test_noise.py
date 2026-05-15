# imports <<<
from pycircuitsim.simulator import NgSpiceSession, simulations
# >>>

# netlisting <<<
netlist = [
    "* Noise Analysis Test",
    "V1 N1 0 1 AC 1 0",
    "R1 N1 out 250",
    "R2 out 0 250",
    ".end"
]
# >>>

# simulation <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Load the netlist into ngspice
session.load_netlist(netlist)

# Initialize a noise simulation object
noise_sim = simulations.Noise(
        output = "V(out)",
        src = "V1",
        sweep_type="dec",
        points = 10,
        fstart = 1,
        fstop = 100e3,
)

# Run simulation
session.run(noise_sim)

# Get the data
data = session.get_all_data()

# Print the data
for k, v in data.data.items():
    print("")
    print(f"{k}: {v}")

# >>>
