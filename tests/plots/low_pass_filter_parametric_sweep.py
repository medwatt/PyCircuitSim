# imports <<<
import numpy as np
import matplotlib.pyplot as plt

from pycircuitsim.simulator import NgSpiceSession, simulations, ParametricSweep
# >>>

# netlist <<<
# RC low-pass filter
netlist = [
    "* RC Low-Pass Filter",
    "V1 in 0 DC 0 AC 1",
    "R1 in out 1k",
    "C1 out 0 100n",
    ".end",
]
# >>>

# simulation <<<
session = NgSpiceSession()
session.load_netlist(netlist)

sweep = ParametricSweep(
    component="R1",
    values=[100, 500, 1000, 5000, 10000],
    simulation=simulations.AC(sweep_type="dec", points=20, fstart=100, fstop=10e6),
)

results = sweep.run(session)
# >>>

# plot <<<
fig, ax = plt.subplots(figsize=(9, 5))

for r_val, data in results.items():
    freq = data.frequency.real
    magnitude_db = 20 * np.log10(np.abs(data.voltages["out"]))
    ax.semilogx(freq, magnitude_db, label=f"R1 = {r_val} Ohm")

ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude (dB)")
ax.set_title("RC Low-Pass Filter")
ax.legend()
ax.grid(True, which="both", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
# >>>
