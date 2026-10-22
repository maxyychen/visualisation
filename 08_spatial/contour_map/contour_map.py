"""
Contour / Isarithmic Map  -  family: Spatial

DESIGN PURPOSE
Draws lines (isolines) or filled bands joining points of equal value over a
continuous surface. The shape of the field (peaks, valleys, gradients) becomes
readable, as on topographic and weather maps.

WHEN TO USE
  - Show a continuous phenomenon that varies smoothly over space (elevation,
    rainfall, temperature, pollution)
  - Show interpolated measurements from sensors or stations
  - Show any 2-D function z = f(x, y), including model response surfaces

AVOID WHEN
  - The data is attached to discrete regions (use a choropleth)
  - There are too few sample points to justify interpolation

ALTERNATIVES
  - Heatmap / raster
  - 3-D surface (rarely better)
  - Hexbin map

EXAMPLE
Synthetic annual rainfall (mm) over a 100 × 80 km region with two mountain
ranges and five towns.

Run:  python contour_map.py
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
rng = np.random.default_rng(4)
x = np.linspace(0, 100, 220); y = np.linspace(0, 80, 180)
X, Y = np.meshgrid(x, y)
def bump(cx, cy, sx, sy, h):
    return h * np.exp(-(((X - cx) / sx) ** 2 + ((Y - cy) / sy) ** 2))
Z = (900 + bump(30, 55, 18, 10, 1600) + bump(75, 25, 12, 16, 1100)
     + bump(55, 70, 25, 8, 500) - 4 * X)
towns = pd.DataFrame({"town": ["Ashford", "Brook", "Calder", "Dunmore", "Elm"],
                      "x": [12, 48, 85, 62, 20], "y": [20, 40, 60, 8, 70]})
towns

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6.2))
levels = np.arange(400, 2700, 250)
cf = ax.contourf(X, Y, Z, levels=levels, cmap=SEQ_CMAP, extend="both")
cs = ax.contour(X, Y, Z, levels=levels[::2], colors="#52514e", linewidths=0.6)
ax.clabel(cs, fmt="%d", fontsize=8)
ax.scatter(towns.x, towns.y, s=40, color=PALETTE[1], edgecolor="#fcfcfb", linewidth=1.5, zorder=3)
for _, t in towns.iterrows():
    ax.annotate(t.town, (t.x, t.y), xytext=(6, 4), textcoords="offset points", fontsize=9,
                fontweight="bold", color="#0b0b0b")
cb = fig.colorbar(cf, ax=ax, shrink=0.85); cb.set_label("Annual rainfall (mm)")
cb.outline.set_visible(False)
ax.set_xlabel("km east"); ax.set_ylabel("km north"); ax.set_aspect("equal")
ax.grid(False)
ax.set_title("Annual rainfall (synthetic)")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
