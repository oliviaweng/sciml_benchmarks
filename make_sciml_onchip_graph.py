import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import math

# Example
# 10 MB MLP model
# 10 MB x 10 MB = 1e7 x 1e7 = 1e14 Ops required
#                             -----------------
# 1e10 Ops x 1e-3 s x 1e10 B/s x 1e-3 s
# --------            --------
# plot                plot
# = 1e7 Op x 1e7 B = 1e14 Ops * B

# 100 KB MLP model
# 100 KB x 100 KB = 1e5 x 1e5 = 1e10 Ops required
# 1e10 Ops x 1e-5 s x 1e10 B/s x 1e-5
# --------            --------
# plot                plot
# = 1e5 x 1e5 = 1e10 Ops

# LHC Sensor
# 1 KB MLP model
# 1 KB * 1 KB = 1e3 * 1e3 = 1e6 Ops required
# 25e12 input data rate (lower bound)
# 25e12 B/s * 1e3 B = 25e15 B/s required
# 1e-8 s requirement
#
# 25e15 B/s * 1e-8 s = 25e7 B
# 1e6 Ops * 1e-8 = 1e-2 Ops
# = 25e7 B * 1e-2 Ops = 25e5 Ops * B
#
# 100e12 input data rate (upper bound)
# 100e12 B/s * 1e3 B = 100e15 B/s required
# 1e-8 s requirement
#
# 100e15 B/s * 1e-8 s = 100e7 B
# 1e6 Ops * 1e-8 = 1e-2 Ops
# = 100e7 B * 1e-2 Ops = 100e5 Ops * B = 1e7

####
# New calculations (input bandwidth + model wt bandwidth)
# LHC Sensor (ECON)
# 2k weights / 25 ns = 80e9

# LHC Trigger (Jet tagger)
# 4k weights / 150 ns = 26e9

# Beam control
# 35k weights / 4 us = 9e9 

# Plasma control
# 13k weights / 7 us = 2e9 

# KWS
# 3e5 weights / 1 ms = 300e6

# AD
# 2e4 weights / 1 ms = 20e6 

# label: data rate lower bound [B/s], data rate upper bound [B/s], latency lower bound [s], latency upper bound [s]
input_dict = {
    # LHC sensor
    # "LHC sensor": [25e12, 100e12, 10e-9, 25e-9],
    # LHC sensor + model
    "LHC sensor": [26e12, 101e12, 10e-9, 25e-9],
    # "LHC near-sensor": [48 * 40e6, 48 * 40e6, 25e-9, 100e-9],
    # "LHC trigger": [32 * 40e6, 32 * 40e6, 100e-9, 5e-6],
    # LHC trigger + model
    "LHC trigger": [32 * 40e6 + 26e9, 32 * 40e6 + 26e9, 100e-9, 5e-6],
    # "Beam Control": [3e3 * 15, 3e3 * 15, 100e-6, 5e-3], # Booster
    # Booster control + model
    "Beam control": [3e3 * 15 + 9e9, 3e3 * 15 + 9e9, 100e-6, 5e-3], # Booster
    # "Magnet quench": [3e6, 3e6, 100e-6, 100e-6],  # Quench
    # "Pixel": [1.28e9/8 * 40/.75, 4*1.28e9/8 * 40/.75, 10e-9, 25e-9],
    # "DUNE": [1e9, 10e9, 1, 5*60],
    # "DUNE readout": [0.8e9, 0.8e9, 1e-6, 1e-6],
    # "Quantum": [1e9, 7e9, 500e-9, 1000e-9], 
    # "Quantum": [40e9, 40e9, 100e-9, 1e-6], 
    # "Qubit Readout": [9e9, 9e9, 100e-9, 100e-9], 
    # "EIC trigger": [7.5e9, 7.5e9, 500e-9, 500e-9], 
    # "X-ray diffraction": [10e6, 100e6, 1e-6, 20e-6],
    # "Electron microscopy": [0.6e9, 0.6e9, 50e-6, 50e-6],
    # "Plasma control": [3e9, 3e9, 5e-6, 20e-6],
    # Plasma control + model
    "Plasma control": [3e9 + 2e9, 3e9 + 2e9, 5e-6, 20e-6],
    # "Neuro": [5e6, 5e6, 1e-3, 1e-3],
    # "Internet-of-things": [3e3 / 100e-3, 3e3 / 1e-3, 1e-3, 100e-3],
    # IoT + KWS
    "Keyword Spotting": [3e3 / 100e-3 + 3e8, 3e3 / 1e-3 + 3e8, 1e-3, 100e-3],
    # IoT + AD
    "Anomoly Detection": [3e3 / 100e-3 + 20e6, 3e3 / 1e-3 + 20e6, 1e-3, 100e-3],
    "Mobile devices": [1e3 / 100e-3, 1e3 / 40e-3, 40e-3, 100e-3],
    # "FF": [10e12, 10e13, 10e-9, 50e-9],
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

ymin = 5e3
ymax = 5e14
xmin = 1e-9
xmax = 1e2


f, ax = plt.subplots()
ax2 = ax.twinx()
# FastML contour
#ax.text(2e-9, 2e10, "FastML Science (WIP)", color="gray", style="italic", weight="bold")
# ax.text(2e-2, 2e13, "Fast ML for Science", color="gray", style="italic", weight="bold")
# ax.text(2e-2, 5e12, "benchmark tasks", color="gray", style="italic", fontsize=22)
# ax.text(2e-2, 5e11, "DRAFT", color="red", style="italic", fontsize=40, alpha=0.5)


# box_y = np.array([3e3 * 15, 3e3 * 15, ymax, ymax])
# box_x = np.array([xmin, 5e-3, 5e-3, xmin])
# ax.fill(box_x, box_y, "gray", alpha=0.2)

# FF - WIP
# ax.text(2e-9, 55e12, "FF", color="blue", style="italic", fontsize=22)
# box_y = np.array([50e12, 50e12, 300e12, 300e12])
# box_x = np.array([1.4e-9, 10e-9, 10e-9, 1.4e-9])
# ax.fill(box_x, box_y, "blue", alpha=0.2)

# BRAM - WIP
# ax.text(1.4e-9, 2e12, "BRAM", color="red", style="italic", fontsize=12)
# box_y = np.array([1e12, 1e12, 10e12, 10e12])
# box_x = np.array([1.4e-9, 10e-9, 10e-9, 1.4e-9])
# ax.fill(box_x, box_y, "red", alpha=0.2)

# DRAM - WIP
# DDR2 - DDR4
# Bandwidth = [3 GB, 25GB]
# Latency = [100ns, 250,000 ns]
# ax.text(1e-6, 7e9, "DRAM", color="green", style="italic", fontsize=16)
# box_y = np.array([3e9, 3e9, 25e9, 25e9])
# box_x = np.array([100e-9, 250000e-9, 250000e-9, 100e-9])
# ax.fill(box_x, box_y, "green", alpha=0.2)

for xloi, xhii, yloi, yhii, l, c in zip(xlo, xhi, ylo, yhi, labels, colors):
    yi = math.sqrt(yloi * yhii)
    xi = math.sqrt(xloi * xhii)
    ax.errorbar(
        [xi],
        [yi],
        yerr=[[yi - yloi], [yhii - yi]],
        xerr=[[xi - xloi], [xhii - xi]],
        # label=l,
        marker="",
        capsize=6,
        markersize=10,
        color=c,
    )
    sz=20.
    if "Internet-of-things" in l:
        # ax.text(xi * 5, yi * 2, l, color=c, size=sz)
        ax.text(xi * 1.1, yi * 2, "IoT", color=c, size=sz)
    if "Keyword Spotting" in l:
        # ax.text(xi * 5, yi * 2, l, color=c, size=sz)
        ax.text(xi * 1.1, yi * 2, "Keyword Spotting", color=c, size=sz)
    elif "Anomoly Detection" in l:
        # ax.text(xi * 5, yi * 2, l, color=c, size=sz)
        ax.text(xi * 1.1, yi * 3, "Anomoly Detection", color=c, size=sz)
    elif "Mobile devices" in l:
        # ax.text(xi * 2, yi * 2, l, color=c, size=sz)
        ax.text(xi * 2, yi * 0.5, "Mobile\ndevices", color=c, size=sz)
    elif "Beam control" in l:
        ax.text(xi * 0.5, yi * 0.5, l, color=c, size=sz)
    elif "LHC sensor" in l:
        # ax.text(xi * 3, yi / 2, l, color=c, size=sz)
        ax.text(xi * 3, yi / 2, "LHC\nsensor", color=c, size=sz)
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
        ax.text(xi, yi * 0.3, l, color=c, size=sz)
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
ax.set_xlabel("Latency requirement [s]")
ax.set_ylabel("Memory bandwidth [B/s]")

ax.axhline(y=10e9, color="green", linestyle="--")
ax.text(1, 5e9, "DRAM", color="green", style="italic", fontsize=18)

ax.axhline(y=10e12, color="red", linestyle="--")
ax.text(1, 5e12, "BRAM", color="red", style="italic", fontsize=18)

ax.axhline(y=300e12, color="blue", linestyle="--")
ax.text(1, 150e12, "FF", color="blue", style="italic", fontsize=18)

# 100 KB model size line (assume fully-connected layer)
# so there are 100k X 100k ops = 10^10 Ops relative to memory bandwidth
# OLD BUGGY
# x_100kb = [1e-9, 1e-6, 10e-6, 10e-3, 10, 1e3]
# y_100kb = [1e15, 1e12, 100e9, 10e7, 1e5, 1e3]
x_100kb = [1e-9, 1e-6, 1e-5, 10e-3, 10, 1e3]
y_100kb = [1e14, 1e11, 1e10, 10e6, 1e4, 1e2]

# 10 MB model
x_10mb = [1e-9, 100e-9, 1e-6, 10e-6, 1e-3, 1e3, 1e5]
y_10mb = [1e16, 100e12, 10e12, 1e12, 10e9, 1e4, 1e2]

ax.plot(x_100kb, y_100kb, linestyle="-", color="purple")
loc_100kb = np.array((1e-2, 10e4))
angle_100kb = 310
ax.text(
    *loc_100kb, 
    "100 KB model size", 
    fontsize=18, 
    rotation=angle_100kb, 
    color="purple",
    # rotation_mode="anchor", 
    # transform_rotates_text=True
)

ax.plot(x_10mb, y_10mb, linestyle="-", color="magenta")
loc_10mb = np.array((0.3, 40e4))
angle_10mb = 310
ax.text(
    *loc_10mb, 
    "10 MB model size", 
    fontsize=18, 
    rotation=angle_10mb, 
    color="magenta",
    # rotation_mode="anchor", 
    # transform_rotates_text=True
)

ax.fill_between(
    x_10mb[:5], 
    y_10mb[:5], 
    [10e9] * 5, 
    interpolate=False, 
    color="red", 
    alpha=0.15,
    label="On-chip inference required"
)

# Second y-axis
ax2.loglog()
ax2.set_ylim(ymin, ymax)
ax2.set_ylabel("Compute Performance [Op/s]")

ax.legend(loc="lower left", fontsize=16)

ax.grid()
plt.tight_layout()
plt.savefig("sciml_onchip_graph.pdf")
plt.savefig("sciml_onchip_graph.png")
