# imports <<<
import matplotlib.pyplot as plt
from pathlib import Path
from pycircuitsim.netlisting import Circuit, SubCircuit
from pycircuitsim.simulator import NgSpiceSession, simulations
# >>>

# netlisting <<<
#-----------------BEGIN---------------------#
inv = SubCircuit(
    name="inverter",
    nodes=["in", "out", "ps", "ns"],
    params={"l_n": "45n", "w_n": "90n", "l_p": "45n", "w_p": "180n"},
)
inv.M("1", ("out", "in", "ns", "ns"), "NMOS_VTH", w="w_n", l="l_n")
inv.M("2", ("out", "in", "ps", "ps"), "PMOS_VTH", w="w_p", l="l_p")
#------------------END----------------------#

circuit = Circuit()
circuit.V("ps", ("ps", "0"), "1")
circuit.V("in", ("in", "0"), "0.5",)
circuit.X("inv", nodes=("in", "out", "ps", "0"), subcircuit=inv, params={"w_n": "500n", "w_p": "1u"})
base_dir = Path(__file__).resolve().parent
circuit.include("./nmos_vth.inc")
circuit.include("./pmos_vth.inc")
# >>>

# build netlist <<<
netlist = circuit.get_netlist()
print(circuit)
# >>>

# simulation <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Load the netlist into ngspice
session.load_netlist(netlist)

# Initialize a DC sweep simulation object
dc_sim = simulations.DC(
    src1 = ("Vin", 0, 1.0, 0.01),
)

# Run a DC sweep
data = session.run(dc_sim)

# Plot <<<
vin  = data.voltages["v-sweep"]
vout = data.voltages["out"]

fig, ax = plt.subplots()
ax.plot(vin, vout)
ax.set_xlabel("V$_{in}$ (V)")
ax.set_ylabel("V$_{out}$ (V)")
ax.set_title("CMOS Inverter DC Transfer Characteristic")
ax.set_xlim(vin[0], vin[-1])
ax.set_ylim(0, 1.05)
ax.grid(True)
plt.tight_layout()
plt.savefig("inverter_dc.svg")
plt.show()
# >>>
