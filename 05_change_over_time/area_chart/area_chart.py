"""
Area Chart  -  family: Change over time

DESIGN PURPOSE
A line chart with the area below the line filled in. The fill stresses volume,
the cumulative size of the quantity over time, not just its trend.

WHEN TO USE
  - Show a single quantity whose magnitude (volume) matters, such as traffic,
    energy, or storage used
  - Emphasise that values are counts or amounts accumulating from zero

AVOID WHEN
  - Comparing several overlapping series (fills hide each other; use lines)
  - The y-axis does not start at zero (a fill implies zero baseline)

ALTERNATIVES
  - Line chart
  - Stacked area chart (several parts of a total)

EXAMPLE
Daily website visits over 6 months.

Run:  python area_chart.py

The notebook also shows this chart built with: plotly, altair.
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
dates = pd.date_range("2024-01-01", periods=182, freq="D")
weekly = 1 + 0.25 * np.sin(2 * np.pi * dates.dayofweek / 7)
visits = (2000 + np.linspace(0, 1500, len(dates))) * weekly + rng.normal(0, 150, len(dates))
df = pd.DataFrame({"date": dates, "visits": visits.round()})
df.head()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.fill_between(df["date"], df["visits"], color=PALETTE[0], alpha=0.25, linewidth=0)
ax.plot(df["date"], df["visits"], color=PALETTE[0], linewidth=1.5)
ax.set_ylim(0, None)
ax.set_ylabel("Visits per day")
ax.set_title("Daily website visits")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
