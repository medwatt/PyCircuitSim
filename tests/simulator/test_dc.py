# imports <<<
from pycircuitsim.simulator import NgSpiceSession, simulations
# >>>

# netlisting <<<
netlist = [
    "* Transistor Sweep",
    "M1 VDN VGN 0 0 NMOS-SH l=1um w=10um",
    "V1 VGN 0 1.5V",
    "V2 VDN 0 2V",
    ".model NMOS-SH nmos (Kp=190u Vto=0.57 Lambda=0.16 Gamma=0.50 Phi=0.7)",
    # ".options savecurrents",
    ".end",
]
# >>>

# simulation <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Load the netlist into ngspice
session.load_netlist(netlist)

# Initialize a DC sweep simulation object
dc_sim = simulations.DC(
    src1 = ("V1", 0, 2, 0.1),
    src2 = ("V2", 0, 2, 0.01)
)

# Run operating point analysis
session.run_simulation(dc_sim)

# Get the data
data = session.get_all_data()

# Print the data
for k, v in data.data.items():
    print("")
    print(f"{k}: {v}")

# >>>>
