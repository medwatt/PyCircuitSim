# imports <<<
from pycircuitsim.simulator import NgSpiceSession, simulations
from pycircuitsim.simulator import VerilogaModel
from pycircuitsim.netlisting.circuit import Circuit
# >>>

# netlisting <<<
myres = VerilogaModel(
    module_name="my_res",
    path="./my_res.va",
    always_recompile=False
)

circuit = Circuit("Operating Point Analysis Test With VerilogA Model")
circuit.V("1", ("in", "0"), "5")
circuit.R("1", ("out", "in"), "2k")
circuit.veriloga("1", ("out", "0"), myres, {"R":"3k"})
circuit.veriloga("2", ("out", "0"), myres, {"R":"5k"})

netlist = circuit.get_netlist()
print(circuit)
# >>>

# simulation <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Add the veriloga model
session.add_veriloga_model(myres)

# Load the netlist into ngspice
session.load_netlist(netlist)

# Run operating point analysis
session.run(simulations.OP())

# Get the data
data = session.get_all_data()

# Print the data
for k, v in data.data.items():
    print("")
    print(f"{k}: {v}")

# >>>>
