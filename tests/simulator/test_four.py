# imports <<<
from pycircuitsim.simulator import NgSpiceSession, simulations
# >>>

# netlisting <<<
# 1kHz sine through an RC low-pass filter
netlist = [
    "* Fourier Analysis Test",
    "V1 in 0 SIN(0 1 1k)",
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

# Fourier requires a preceding transient simulation
tran_simulation = simulations.Tran(
    tstep=1e-6,
    tstop=10e-3,
)
session.run_simulation(tran_simulation)

four_simulation = simulations.Four(
    freq=1e3,
    output_variables="V(out)",
    n_harmonics=9,
)

# Run simulation
session.run_simulation(four_simulation)

# Get the data
data = session.get_all_data()

# Print the data
for k, v in data.data.items():
    print("")
    print(f"{k}: {v}")

# >>>
