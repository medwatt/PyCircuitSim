# imports <<<
from pycircuitsim.simulator import NgSpiceSession
from pycircuitsim.simulator import VerilogaModel
# >>>

# netlisting <<<
netlist = [
    "* Operating Point Analysis Test With VerilogA Model",
    "V1 in 0 5",
    "R1 out in 2k",
    "N1 out 0 res_model",
    ".model res_model my_res R=3k",
    ".end",
]
# >>>

# simulation <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Add veriloga model
myres = VerilogaModel(
    module_name="my_res",
    path="./my_res.va",
    always_recompile=False
)
session.add_veriloga_model(myres)

# Load the netlist into ngspice
session.load_netlist(netlist)

# Run operating point analysis
session.run_simulation()

# Get the data
data = session.get_all_data()

# Print the data
for k, v in data.data.items():
    print("")
    print(f"{k}: {v}")

# >>>>
