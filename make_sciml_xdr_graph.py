import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import math

# label: data rate lower bound [B/s], data rate upper bound [B/s], latency lower bound [s], latency upper bound [s]
input_dict = {
    "LHC sensor": [25e12, 100e12, 10e-9, 25e-9],
    # "LHC near-sensor": [48 * 40e6, 48 * 40e6, 25e-9, 100e-9],
    "LHC trigger": [32 * 40e6, 32 * 40e6, 100e-9, 5e-6],
    # "Beam Control": [3e3 * 15, 3e3 * 15, 100e-6, 5e-3], # Booster
    "Beam control": [3e3 * 15, 3e3 * 15, 100e-6, 5e-3], # Booster control
    "Magnet quench": [3e6, 3e6, 100e-6, 100e-6],  # Quench
    # "Pixel": [1.28e9/8 * 40/.75, 4*1.28e9/8 * 40/.75, 10e-9, 25e-9],
    # "DUNE": [1e9, 10e9, 1, 5*60],
    "DUNE readout": [0.8e9, 0.8e9, 1e-6, 1e-6],
    # "Quantum": [1e9, 7e9, 500e-9, 1000e-9], 
    # "Quantum": [40e9, 40e9, 100e-9, 1e-6], 
    "Qubit Readout": [9e9, 9e9, 100e-9, 100e-9], 
    "EIC trigger": [7.5e9, 7.5e9, 500e-9, 500e-9], 
    "X-ray diffraction": [10e6, 100e6, 1e-6, 20e-6],
    "Electron microscopy": [0.6e9, 0.6e9, 50e-6, 50e-6],
    "Plasma control": [3e9, 3e9, 5e-6, 20e-6],
    "Neuro": [5e6, 5e6, 1e-3, 1e-3],
    "Internet-of-things": [3e3 / 100e-3, 3e3 / 1e-3, 1e-3, 100e-3],
    "Mobile devices": [1e3 / 100e-3, 1e3 / 40e-3, 40e-3, 100e-3],
}
labels = input_dict.keys()
ylo = np.array([input_dict[key][0] for key in labels])
yhi = np.array([input_dict[key][1] for key in labels])
xlo = np.array([input_dict[key][2] for key in labels])
xhi = np.array([input_dict[key][3] for key in labels])

colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#17becf",
    "#7f7f7f",
    "#bcbd22",
    "#d62728",
]
### get more
colors += ["#1f77b4","#9467bd","#bcbd22","#17becf","#ff7f0e",]
colors += ["#bbbbbb"]*10

plt.style.use([hep.style.ROOT, hep.style.firamath])

ymin = 1e2
ymax = 2e14
xmin = 1e-9
xmax = 1e5


f, ax = plt.subplots()
# FastML contour
#ax.text(2e-9, 2e10, "FastML Science (WIP)", color="gray", style="italic", weight="bold")
ax.text(2e-2, 2e13, "Fast ML for Science", color="gray", style="italic", weight="bold")
ax.text(2e-2, 5e12, "benchmark tasks", color="gray", style="italic", fontsize=22)
box_y = np.array([3e3 * 15, 3e3 * 15, ymax, ymax])
box_x = np.array([xmin, 5e-3, 5e-3, xmin])
ax.fill(box_x, box_y, "gray", alpha=0.2)

for xloi, xhii, yloi, yhii, l, c in zip(xlo, xhi, ylo, yhi, labels, colors):
    yi = math.sqrt(yloi * yhii)
    xi = math.sqrt(xloi * xhii)
    ax.errorbar(
        [xi],
        [yi],
        yerr=[[yi - yloi], [yhii - yi]],
        xerr=[[xi - xloi], [xhii - xi]],
        label=l,
        marker="",
        capsize=6,
        markersize=10,
        color=c,
    )
    sz=20.
    if "Internet-of-things" in l:
        ax.text(xi * 5, yi * 2, l, color=c, size=sz)
    elif "Mobile devices" in l:
        ax.text(xi * 2, yi * 2, l, color=c, size=sz)
    elif "Beam control" in l:
        ax.text(xi / 5e3, yi * 2, l, color=c, size=sz)
    elif "LHC sensor" in l:
        ax.text(xi * 3, yi / 2, l, color=c, size=sz)
    elif "LHC near-sensor" in l:
        ax.text(xi / 20, yi * 3.5, "LHC", color=c, size=sz)
        ax.text(xi / 20, yi * 1.5, "near-sensor", color=c, size=sz)
    elif "X-ray diffraction" in l:
        ax.text(xi * 3, yi * 1.6, "X-ray diffraction", color=c, size=sz)
        # ax.text(xi / 2e3, yi / 2, "(BraggNN)", color=c, size=sz)
    elif "EIC trigger" in l:
        ax.text(xi / 100, yi / 3, l, color=c, size=sz)
    elif "Qubit Readout" in l:
        ax.text(xi / 10, yi * 1.9, l, color=c, size=sz)
    elif "Plasma control" in l:
        ax.text(xi * 3, yi * 1, l, color=c, size=sz)
    elif "DUNE readout" in l:
        ax.text(xi / 5e2, yi / 3, l, color=c, size=sz)
    elif "DUNE" in l:
        ax.text(xi / 1e2, yi / 6, l, color=c, size=sz)
    elif "LHC trigger" in l:
        ax.text(xi * 10, yi / 1.2, l, color=c, size=sz)
    elif "Magnet quench" in l:
        ax.text(xi / 1e3, yi / 4, l, color=c, size=sz)
    elif "Electron microscopy" in l:
        ax.text(xi * 1.5, yi / 2, l, color=c, size=sz)
    elif "Neuro" in l:
        ax.text(xi / 5, yi * 1.7, l, color=c, size=sz)
    else:
        ax.text(xi * 1, yi * 1, l, color=c, size=sz)
    # ax.text(xi * 2, yi * 2, l, color=c, size=10.)

ax.loglog()
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_xlabel("Computation time [s]")
ax.set_ylabel("Data rate [B/s]")

plt.tight_layout()
plt.savefig("sciml_graph.pdf")
plt.savefig("sciml_graph.png")
