"""
Streamgraph  -  family: Change over time

DESIGN PURPOSE
A stacked area chart laid out around a central, wiggling baseline instead of
zero. It gives an organic, flowing picture of how many categories rise and
fall over time.

WHEN TO USE
  - Show the ebb and flow of many categories over time (music genres, topics,
    species)
  - Engaging, editorial graphics where overall patterns matter more than exact
    values

AVOID WHEN
  - Precise values or totals must be read (there is no fixed baseline)
  - Analytical or dashboard contexts
  - There are few time points

ALTERNATIVES
  - Stacked area chart
  - Small multiples
  - Heatmap

EXAMPLE
Weekly listening share of six music genres across a year.

Run:  python streamgraph.py
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
rng = np.random.default_rng(12)
weeks = np.arange(52)
genres = ["Pop", "Rock", "Hip-hop", "Electronic", "Jazz", "Classical"]
def bump(center, width, height):
    return height * np.exp(-((weeks - center) / width) ** 2)
df = pd.DataFrame({g: bump(rng.uniform(5, 47), rng.uniform(6, 14), rng.uniform(20, 60))
                   + rng.uniform(5, 15) for g in genres}, index=weeks)
df.head()

# --- Plot --------------------------------------------------------------------
from scipy.ndimage import gaussian_filter1d
smooth = df.apply(lambda s: gaussian_filter1d(s, 1.5))
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.stackplot(smooth.index, smooth.T.values, baseline="wiggle", labels=smooth.columns,
             colors=PALETTE[:6], edgecolor="#fcfcfb", linewidth=0.8)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Week of year")
ax.set_xlim(0, 51)
ax.set_title("Listening by genre over the year")
ax.legend(loc="upper left", ncol=6, bbox_to_anchor=(0, -0.15))
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
