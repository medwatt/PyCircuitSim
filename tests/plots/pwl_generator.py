# imports <<<
import matplotlib.pyplot as plt

from pycircuitsim.simulator import NgSpiceSession, simulations
from pycircuitsim.netlisting import Circuit
from pycircuitsim.netlisting import WaveformGenerator
# >>>

# circuit definition <<<
circuit = Circuit("PWL waveform generator test")

waveform = WaveformGenerator(scale="m", transition_time=0.001, dc_baseline=0)
waveform.delay(duration=1)
waveform.triangle(duration=8, peak_value=2, cycles=1)
waveform_data = waveform.generate()

circuit.VoltagePWL("1", ("nin", "0"), time_value_pairs=waveform_data)
circuit.R("1", ("nin", "0"), "1k")
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
    tstop = 10e-3,
    tstep = 1e-3,
)

# Run simulation
data = session.run(tran_simulation)

# Plot the waveform
plt.plot(data.time, data.voltages["nin"])
plt.show()
# >>>
