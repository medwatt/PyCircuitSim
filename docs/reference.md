# PyCircuitSim Reference

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Netlisting](#netlisting)
   - [Raw netlists](#raw-netlists)
   - [Circuit class](#circuit-class)
   - [Components](#components)
   - [SubCircuit](#subcircuit)
   - [WaveformGenerator](#waveformgenerator)
4. [Simulation](#simulation)
   - [NgSpiceSession](#ngspicesession)
   - [Simulation types](#simulation-types)
   - [Accessing results](#accessing-results)
5. [Advanced features](#advanced-features)
   - [ParametricSweep](#parametricsweep)
   - [CornerAnalysis](#corneranalysis)
   - [ParameterModifier](#parametermodifier)
   - [VerilogaModel](#verilogamodel)

---

## Overview

PyCircuitSim wraps the ngspice shared library (`libngspice`) to offer a
Python-native workflow for analog circuit simulation. There are two ways to
define a circuit:

- **Raw netlists**: pass a list of SPICE strings directly, which is useful
when you already have a netlist or want full control over the syntax.

- **Circuit API**: build the circuit programmatically using Python
objects, which avoids manual string formatting and makes parameterisation
easier.

Both approaches produce the same result: a list of strings that is loaded into
an `NgSpiceSession`.

---

## Installation

ngspice must be compiled with shared library support before installing PyCircuitSim:

```bash
# Build ngspice with shared library support
./configure --with-ngshared
make && make install
```

Then install PyCircuitSim:

```bash
pip install git+https://github.com/medwatt/PyCircuitSim.git
```

---

## Netlisting

### Raw netlists

The simplest approach is to pass a list of SPICE strings to
`session.load_netlist()`. Every netlist must begin with a title line and end
with `.end`.

```python
netlist = [
    "* RC Low-Pass Filter",
    "V1 in 0 DC 0 AC 1",
    "R1 in out 1k",
    "C1 out 0 100n",
    ".end",
]
```

A plain string with newlines is also accepted:

```python
netlist = """\
* RC Low-Pass Filter
V1 in 0 DC 0 AC 1
R1 in out 1k
C1 out 0 100n
.end"""
```

### Circuit class

`Circuit` builds a netlist programmatically. Components are added as method
calls. Call `get_netlist()` to obtain the list of strings for `load_netlist()`,
or `print(circuit)` to get the SPICE text.

```python
from pycircuitsim.netlisting import Circuit

circuit = Circuit("Half-wave rectifier")

circuit.VoltageSin("1", ("nin", "0"), amplitude="1", frequency="1k")
circuit.R("1", ("nin", "nout"), "1k")
circuit.D("1", ("nout", "0"), model_name="D")
circuit.define_model(model_name="D", model_type="D", RS="10")

print(circuit)           # inspect SPICE text
netlist = circuit.get_netlist()
```

`.include`, `.lib`, and `.param` can be added through dedicated methods:

```python
circuit.include("/path/to/models.lib")
circuit.lib("/path/to/process.lib", section="tt")
circuit.param(VDD="1.8", TEMP="27")
```

### Components

All component constructors share the signature `(id, nodes, value_or_model,
**params)`. The `id` is the numeric or alphanumeric suffix appended to the
component letter (e.g. `"1"` → `R1`). Nodes are given as a tuple of node
name strings.

#### Passive

```python
from pycircuitsim.netlisting.components.passive import (
    Resistor, Inductor, Capacitor,
    MutualInductance,
    VoltageControlledSwitch, CurrentControlledSwitch,
    LosslessTransmissionLine,
)

Resistor("1", ("a", "b"), "1k")                        # R1 a b 1k
Resistor("1", ("a", "b"), "1k", temp="25")             # R1 a b 1k temp=25
Inductor("1", ("a", "b"), "1u")                        # L1 a b 1u
Capacitor("1", ("a", "b"), "1n")                       # C1 a b 1n
MutualInductance("1", "1", "2", "0.9")                 # K1 L1 L2 0.9

VoltageControlledSwitch("1", ("n1", "n2", "nc1", "nc2"), "MYSW")
CurrentControlledSwitch("1", ("n1", "n2"), "Vctrl", "MYSW")

LosslessTransmissionLine("1", ("in", "0", "out", "0"), "50", td="1ns")
LosslessTransmissionLine("1", ("in", "0", "out", "0"), "75", frequency="1e9")
```

These are available as methods on `Circuit` and `SubCircuit` without the
explicit import:

```python
circuit.R("1", ("a", "b"), "1k")
circuit.C("1", ("out", "0"), "100n")
circuit.L("1", ("a", "b"), "1u")
```

#### Semiconductors

```python
from pycircuitsim.netlisting.components.semiconductors import Diode, JFET, Mosfet, BJT

Diode("1", ("anode", "cathode"), "D1N4148")
JFET("1", ("d", "g", "s"), "NJFET")
Mosfet("1", ("d", "g", "s", "b"), "NMOS", l="1u", w="10u")
BJT("1", ("c", "b", "e"), "NPN")
```

Or via `Circuit`:

```python
circuit.D("1", ("anode", "cathode"), model_name="D1N4148")
circuit.M("1", ("d", "g", "s", "b"), model_name="NMOS", l="1u", w="10u")
circuit.Q("1", ("c", "b", "e"), model_name="NPN")
```

Models are declared with `define_model`:

```python
circuit.define_model(model_name="NMOS", model_type="nmos", Kp="190u", Vto="0.57")
```

#### Independent sources

```python
from pycircuitsim.netlisting.components.independent import (
    VoltageSource, CurrentSource,
    VoltagePulse, CurrentPulse,
    VoltageSin, CurrentSin,
    VoltageExp, CurrentExp,
    VoltagePWL, CurrentPWL,
    VoltageTransientNoise, CurrentTransientNoise,
)

# DC source with optional AC magnitude
VoltageSource("1", ("in", "0"), dc_value="1.8", ac_magnitude="1")

# Sinusoidal
VoltageSin("1", ("in", "0"), amplitude="1", frequency="1k")

# Pulse
VoltagePulse("1", ("in", "0"), v1="0", v2="3.3", td="0", tr="1n", tf="1n", pw="500n", per="1u")

# Piecewise linear: pass a list of (time, value) pairs
VoltagePWL("1", ("in", "0"), time_value_pairs=[(0, 0), (1e-3, 1), (2e-3, 0)])
```

#### Dependent sources

```python
from pycircuitsim.netlisting.components.dependent import (
    VoltageControlledVoltageSource,
    VoltageControlledCurrentSource,
    CurrentControlledVoltageSource,
    CurrentControlledCurrentSource,
    BehavioralSource,
)

VoltageControlledVoltageSource("1", ("out", "0", "in", "0"), gain="10")
BehavioralSource("1", ("out", "0"), expression="V(a)*V(b)")
```

### SubCircuit

`SubCircuit` defines a reusable block. It accepts an optional `params` dict
of default parameter values. Instances are created with `circuit.X(...)`.

```python
from pycircuitsim.netlisting import Circuit, SubCircuit

# Define a subcircuit
rc = SubCircuit(
    name="rc_stage",
    nodes=["in", "out"],
    params={"Rval": "1k", "Cval": "1u"}
)
rc.R("1", ("in", "out"), "{Rval}")
rc.C("1", ("out", "0"), "{Cval}")

# Instantiate it in a top-level circuit
circuit = Circuit()
circuit.X("stage1", nodes=("in", "out"), subcircuit=rc)
circuit.X("stage2", nodes=("in", "out"), subcircuit=rc, params={"Rval": "2k"})

circuit.V("1", ("in", "0"), "1", ac_magnitude="1")
```

SubCircuits can be nested: a `SubCircuit` can instantiate another
`SubCircuit` via `.X(...)`.

### WaveformGenerator

`WaveformGenerator` builds a piecewise-linear (PWL) waveform programmatically
and returns a list of `(time, value)` pairs that can be passed to
`VoltagePWL` or `CurrentPWL`.

```python
from pycircuitsim.netlisting import WaveformGenerator

waveform = WaveformGenerator(scale="m", transition_time=0.001, dc_baseline=0)
waveform.delay(duration=1)
waveform.triangle(duration=8, peak_value=2, cycles=1)

pwl_data = waveform.generate()
circuit.VoltagePWL("1", ("in", "0"), time_value_pairs=pwl_data)
```

The `scale` parameter sets the time unit (`"m"` = milliseconds, `"u"` =
microseconds, etc.).

---

## Simulation

### NgSpiceSession

`NgSpiceSession` is the entry point to ngspice. It manages the lifetime of
the shared library and exposes methods to load netlists, send commands, and
retrieve results.

```python
from pycircuitsim.simulator import NgSpiceSession

session = NgSpiceSession()
# Optionally provide an explicit path to libngspice:
# session = NgSpiceSession(libpath="/usr/local/lib/libngspice.so")
```

Key methods:

| Method | Description |
|--------|-------------|
| `load_netlist(netlist)` | Load a netlist (list of strings or newline-separated string) |
| `run_simulation(sim)` | Run a simulation and return the organised result object |
| `send_command(cmd)` | Send an arbitrary ngspice command string |
| `get_all_data(plot_name=None)` | Retrieve all vectors from the current (or named) plot |
| `get_vector_names(plot_name=None)` | List vector names in a plot |
| `get_data(vector_name)` | Retrieve a single vector as a numpy array |
| `get_current_plot_name()` | Return the name of the active plot |
| `get_all_plot_names()` | Return names of all plots in the session |

### Simulation types

All simulation classes live in `pycircuitsim.simulator.simulations`.

#### Operating point: `OP`

```python
from pycircuitsim.simulator import simulations

data = session.run_simulation(simulations.OP())
# data.voltages : dict of node voltages
# data.currents : dict of branch currents
```

#### DC sweep: `DC`

Sweeps one or two independent sources.

```python
dc = simulations.DC(
    src1=("V1", 0, 2, 0.1),          # (source, start, stop, step)
    src2=("V2", 0, 2, 0.01),         # optional second sweep
)
data = session.run_simulation(dc)
```

#### AC analysis: `AC`

```python
ac = simulations.AC(
    sweep_type="dec",   # "dec", "lin", or "oct"
    points=20,
    fstart=1,
    fstop=1e6,
)
data = session.run_simulation(ac)
# data.frequency : numpy array of frequency points
# data.voltages  : dict of complex node voltages
# data.currents  : dict of complex branch currents
```

#### Transient analysis: `Tran`

```python
tran = simulations.Tran(
    tstep=1e-6,
    tstop=1e-3,
    tstart=None,   # optional: time at which to start saving data
    tmax=None,     # optional: maximum internal timestep
    uic=False,     # use initial conditions
)
data = session.run_simulation(tran)
# data.time     : numpy array of time points
# data.voltages : dict of node voltages (numpy arrays)
# data.currents : dict of branch currents (numpy arrays)
```

#### Transfer function: `TF`

```python
tf = simulations.TF(output_variable="V(out)", input_source="V1")
data = session.run_simulation(tf)
```

#### Pole-zero analysis: `PZ`

```python
pz = simulations.PZ(
    nodes=("in", "0", "out", "0"),
    source_type="vol",    # "vol" or "cur"
    analysis_type="pz",   # "pol", "zer", or "pz"
)
data = session.run_simulation(pz)
```

#### Sensitivity analysis: `Sens`

```python
sens = simulations.Sens(output_variable="V(out)")
data = session.run_simulation(sens)
```

#### Fourier analysis: `Four`

Must be run after a transient simulation on the same session.

```python
session.run_simulation(simulations.Tran(tstep=1e-6, tstop=1e-3))
four = simulations.Four(freq=1e3, output_variables=["V(out)"], n_harmonics=9)
data = session.run_simulation(four)
```

#### Noise analysis: `Noise`

```python
noise = simulations.Noise(
    output="V(out)",
    src="V1",
    sweep_type="dec",
    points=10,
    fstart=1,
    fstop=1e6,
)
data = session.run_simulation(noise)
```

### Accessing results

`run_simulation()` returns a data organizer object whose available attributes
depend on the simulation type.


| Attribute | Available in |
|-----------|-------------|
| `data.voltages` | All simulation types |
| `data.currents` | All simulation types |
| `data.time` | `Tran` |
| `data.frequency` | `AC`, `Noise` |
| `data.parameters` | `AC`, `Tran` |
| `data.data` | All types: raw dict of all vectors |


Voltages are keyed by node name. For flat circuits the key is a string; for
hierarchical circuits with subcircuits the result is a nested dict mirroring
the instance hierarchy:

```python
# Flat circuit
v_out = data.voltages["out"]

# Hierarchical circuit (subcircuit instance xtop containing xsub)
v_node = data.voltages["xtop"]["xsub"]["node"]
```

Currents are keyed by the source name (e.g. `"v1"` for `V1`).

---

## Advanced features

### ParametricSweep

Runs the same simulation repeatedly while sweeping a single component value.
Returns a dict keyed by the swept value.

```python
from pycircuitsim.simulator import ParametricSweep

sweep = ParametricSweep(
    component="R1",
    values=[100, 500, 1000, 5000, 10000],
    simulation=simulations.AC(sweep_type="dec", points=20, fstart=100, fstop=10e6),
)

results = sweep.run(session)

for r_val, data in results.items():
    print(r_val, data.voltages["out"])
```

For components inside subcircuit hierarchies, use the full ngspice alter
expression:

```python
sweep = ParametricSweep(
    component="@r.xtop.xstage.r1[resistance]",
    values=[1e3, 2e3, 5e3],
    simulation=simulations.AC(sweep_type="dec", points=10, fstart=1, fstop=1e6),
)
```

### CornerAnalysis

Runs a simulation at each named corner, where each corner defines a set of
component value overrides. Returns a dict keyed by corner name.

```python
from pycircuitsim.simulator import CornerAnalysis

corners = CornerAnalysis(
    corners={
        "slow":    {"R1": 1200, "C1": 120e-9},
        "typical": {"R1": 1000, "C1": 100e-9},
        "fast":    {"R1":  800, "C1":  80e-9},
    },
    simulation=simulations.AC(sweep_type="dec", points=20, fstart=100, fstop=1e6),
)

results = corners.run(session)

for corner, data in results.items():
    print(corner, data.voltages["out"])
```

### ParameterModifier

Modifies component parameters inside a subcircuit hierarchy after the netlist
has been loaded. Use this to alter deep instance parameters between simulation
runs without reloading the netlist.

```python
from pycircuitsim.simulator import ParameterModifier

modifier = ParameterModifier(
    hierarchical_name=("xtop", "xstage", "xrc"),
    parameter_changes={
        "R1": "2k",
        "C1": "50n",
    },
)

commands = modifier.get_alter_commands()
session.send_command(commands)

data = session.run_simulation(simulations.AC(sweep_type="dec", points=10, fstart=1, fstop=1e6))
```

### VerilogaModel

Compiles and loads an OpenVAF/OSDI Verilog-A model before the netlist is
loaded.

```python
from pycircuitsim.simulator import VerilogaModel

model = VerilogaModel(source_path="/path/to/model.va")
session.add_veriloga_model(model)

# load_netlist compiles and loads all registered models automatically
session.load_netlist(netlist)
```
