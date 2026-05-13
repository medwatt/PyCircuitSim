# imports <<<
import matplotlib.pyplot as plt

from pycircuitsim.simulator import NgSpiceSession, simulations
from pycircuitsim.netlisting import Circuit
# >>>

# circuit definition <<<
circuit = Circuit("Half-wave rectifier circuit")
circuit.VoltageSin("1", ("nin", "0"), amplitude="1", frequency="1k")
circuit.R("1", ("nin", "nout"), "1k")
circuit.D("1", ("nout", "0"), model_name="D")
circuit.define_model(model_name="D", model_type="D", RS="10")
# >>>

# build netlist <<<
print(circuit)
netlist = circuit.get_netlist()
# >>>

# simulate <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Load the netlist into ngspice
session.load_netlist(netlist)

# Simulate for 1ms
tran_simulation = simulations.Tran(
    tstop = 1e-3,
    tstep = 1e-3,
)

# Run simulation
data = session.run(tran_simulation)

# Plot the waveform
plt.plot(data.time, data.voltages["nout"])
plt.show()
# >>>
