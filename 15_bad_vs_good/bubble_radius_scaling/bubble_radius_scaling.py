"""
Bubble Scaled by Radius vs. by Area  -  family: Bad vs. good

DESIGN PURPOSE
Readers judge a circle by its area. If the radius (or diameter) is made
proportional to the value, the area grows with the square of the value, so a
value twice as large looks four times as large and an 8× difference looks like
a 64× difference.

WHEN TO USE
  - Scale bubble AREA proportional to value (radius ∝ √value) in bubble
    charts, bubble maps and packed circles
  - Use bars instead when precise comparison matters, since people
    underestimate area differences even when area is scaled correctly

AVOID WHEN
  - Hand-built bubble charts that set radius or diameter from the value
  - Icons or pictograms scaled in both width and height by the value

ALTERNATIVES
  - Bar chart (precise comparison)
  - Area-scaled bubbles with a size legend
  - Pictogram / isotype (count icons instead of scaling one)

EXAMPLE
Annual patient volume of four clinics (1k, 2k, 4k and 8k).

Run:  python bubble_radius_scaling.py
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
df = pd.DataFrame({"clinic": ["Clinic A", "Clinic B", "Clinic C", "Clinic D"],
                   "patients_k": [1, 2, 4, 8]})
df

# --- Plot --------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
xs = np.array([0.5, 1.6, 3.0, 5.0])
for ax, mode in [(ax1, "radius"), (ax2, "area")]:
    v = df["patients_k"].to_numpy()
    radius = 0.11 * v if mode == "radius" else 0.31 * np.sqrt(v)   # data units
    for x, r, name, val in zip(xs, radius, df["clinic"], v):
        ax.add_patch(plt.Circle((x, r), r, color=PALETTE[0] if mode == "area" else PALETTE[7],
                                alpha=0.85, linewidth=0))
        ax.text(x, -0.25, f"{name}\n{val}k", ha="center", va="top", fontsize=9.5, color="#52514e")
    ax.set_xlim(-0.3, 6.1)
    ax.set_ylim(-0.75, 2.0)
    ax.set_aspect("equal")
    ax.axis("off")
ax1.set_title("✗ Misleading: radius ∝ value (8× looks like 64×)", fontsize=11.5)
ax2.set_title("✓ Better: area ∝ value (8× looks like 8×)", fontsize=11.5)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
