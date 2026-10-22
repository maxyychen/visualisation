"""
Barcode Plot (Rug Plot)  -  family: Distribution

DESIGN PURPOSE
Draws each observation as a thin vertical tick on a line. It is a minimal,
high-resolution distribution display that also works well for placing one item
among the rest.

WHEN TO USE
  - Show exactly where individual values fall, for example to highlight one
    country among all of them
  - Show a compact distribution strip for dashboards and tables
  - Add a margin to a density or scatter plot

AVOID WHEN
  - There are many duplicate or close values (ticks overlap and hide counts)
  - The audience needs the shape (add a density curve)

ALTERNATIVES
  - Dot strip plot
  - Histogram
  - Beeswarm

EXAMPLE
Unemployment rate of 50 US-like states on three dates, highlighting one state
(simulated).

Run:  python barcode_plot.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Library style: categorical colors in fixed order, recessive axes, hairline grid.
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
           "#e87ba4", "#008300", "#6250d6", "#e34948"]
SEQ_CMAP = "Blues"      # sequential: one hue, light -> dark
DIV_CMAP = "RdBu_r"     # diverging: two opposite hues, neutral midpoint
GRAY = "#b8b7b1"        # de-emphasised marks
plt.rcParams.update({
    "figure.figsize": (8, 4.8), "figure.dpi": 110, "figure.facecolor": "#fcfcfb",
    "axes.facecolor": "#fcfcfb", "axes.edgecolor": "#c9c8c3", "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#e6e5e1", "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.prop_cycle": plt.cycler(color=PALETTE),
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#52514e",
    "text.color": "#0b0b0b", "font.size": 10, "lines.linewidth": 2,
    "legend.frameon": False,
})

# --- Example data ------------------------------------------------------------
rng = np.random.default_rng(41)
dates = ["Jan 2020", "Apr 2020", "Jan 2022"]
centers = [3.6, 13.0, 4.2]
spreads = [0.8, 3.5, 1.0]
df = pd.concat([pd.DataFrame({"date": d, "state": [f"S{i:02d}" for i in range(50)],
                              "rate": rng.normal(c, s, 50).clip(1.5)})
                for d, c, s in zip(dates, centers, spreads)], ignore_index=True)
focus = "S07"
df[df["state"] == focus]

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 3.6))
for y, d in enumerate(dates):
    g = df[df["date"] == d]
    ax.vlines(g["rate"], y - 0.3, y + 0.3, color=GRAY, linewidth=1.5)
    f = g[g["state"] == focus]["rate"].iloc[0]
    ax.vlines(f, y - 0.38, y + 0.38, color=PALETTE[1], linewidth=3)
    if y == 0:
        ax.text(f, y + 0.45, focus, ha="center", fontsize=9, color="#0b0b0b", weight="bold")
ax.set_yticks(range(len(dates)), dates)
ax.invert_yaxis()
ax.set_xlabel("Unemployment rate (%)")
ax.set_title(f"State unemployment rates ({focus} highlighted)")
ax.grid(axis="y", visible=False)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
