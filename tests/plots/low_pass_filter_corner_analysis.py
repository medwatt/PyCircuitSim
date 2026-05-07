# imports <<<
import numpy as np
import matplotlib.pyplot as plt

from pycircuitsim.simulator import NgSpiceSession, simulations, CornerAnalysis
# >>>

# netlist <<<
# RC low-pass filter with nominal R=1k, C=100n -> fc ≈ 1.59 kHz
netlist = [
    "* Corner Analysis — RC Low-Pass Filter",
    "V1 in 0 DC 0 AC 1",
    "R1 in out 1k",
    "C1 out 0 100n",
    ".end",
]
# >>>

# simulation <<<
session = NgSpiceSession()
session.load_netlist(netlist)

corners = CornerAnalysis(
    corners={
        "slow": {"R1": 1200, "C1": 120e-9},
        "typical": {"R1": 1000, "C1": 100e-9},
        "fast": {"R1": 800, "C1": 80e-9},
    },
    simulation=simulations.AC(sweep_type="dec", points=20, fstart=100, fstop=1e6),
)

results = corners.run(session)
# >>>

# plot <<<
fig, ax = plt.subplots(figsize=(9, 5))

for corner, data in results.items():
    freq = data.frequency.real
    magnitude_db = 20 * np.log10(np.abs(data.voltages["out"]))
    ax.semilogx(freq, magnitude_db, label=corner)

ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude (dB)")
ax.set_title("RC Low-Pass Filter: Corner Analysis")
ax.legend()
ax.grid(True, which="both", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
# >>>
