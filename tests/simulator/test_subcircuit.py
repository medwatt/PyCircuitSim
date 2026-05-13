# imports <<<
from pycircuitsim.simulator import NgSpiceSession, simulations, ParameterModifier
from pycircuitsim.netlisting import Circuit, SubCircuit
# >>>

# cells <<<

#-----------------BEGIN---------------------#
c0 = SubCircuit(
    name='rc_stage',
    nodes=['in', 'out'],
    params={'Rval': '1k', 'Cval': '1u'}
)
c0.R("1", ('in', 'out'), '{Rval}')
c0.C("1", ('out', '0'), '{Cval}')
#------------------END----------------------#

#-----------------BEGIN---------------------#
c1 = SubCircuit(
    name='rc_stage_modified',
    nodes=['in', 'out'],
    params={
        'Rval': '1k',
    },
)
c1.X(
    id='c0_1',
    nodes=('in', 'n1'),
    subcircuit=c0,
    params={'Rval': '2k', 'Cval': '3u'}
)
c1.R("1", ('n1', 'out'), '{Rval}')
#------------------END----------------------#

#-----------------BEGIN---------------------#
top = SubCircuit(
    name='topcell',
    nodes=['in1', 'out1', 'in2', 'out2'],
)
top.X(
    id='c1_1',
    nodes=('in1', 'out1'),
    subcircuit=c1
)
top.X(
    id='c1_2',
    nodes=('in2', 'out2'),
    subcircuit=c1,
    params={'Rval': '2k'}
)
top.V("1", ('in1', '0'), "1", ac_magnitude="1")
top.V("2", ('in2', '0'), "1", ac_magnitude="1")
#------------------END----------------------#

circuit = Circuit()
circuit.X('top', nodes=('in1', 'out1', 'in2', 'out2'), subcircuit=top)

# >>>

# build netlist <<<
netlist = circuit.get_netlist()
print(circuit)
# >>>

# simulate <<<

# Instantiate an ngspice object
session = NgSpiceSession()

# Load the netlist into ngspice
session.load_netlist(netlist)

# Initialize a DC sweep simulation object
ac_sim = simulations.AC(
    sweep_type = 'dec',
    points = 10,
    fstart = 1,
    fstop = 1e6,
)

# Run simulation
session.run(ac_sim)

# Get the data
data = session.get_all_data()

# Print result
print(data.voltages["xtop"]["xc1_1"]["n1"])

# >>>

# modify <<<

# Modify parameters
parameter_modifier = ParameterModifier(
    hierarchical_name=("xtop", "xc1_1", "xc0_1"),
    parameter_changes={
        "R1": "1",
        "C1": "100u",
    },
)

alter_commands = parameter_modifier.get_alter_commands()
print(alter_commands)

session.send_command(alter_commands)

# Run simulation
session.run(ac_sim)

# Get the data
data = session.get_all_data()

# Print result
print(data.voltages)
# print(data.voltages["xtop"]["xc1_1"]["n1"])
# >>>
