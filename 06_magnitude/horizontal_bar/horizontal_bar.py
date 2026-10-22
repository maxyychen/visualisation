"""
Horizontal Bar Chart (sorted)  -  family: Magnitude

DESIGN PURPOSE
Bars laid out horizontally and sorted by value. Long category labels stay
readable, and the sort turns the chart into a ranking as well as a size
comparison.

WHEN TO USE
  - Category names are long (countries, products, survey answers)
  - There are many categories (up to ~25)
  - Show both size and rank at once

AVOID WHEN
  - Categories have a natural order such as time (keep that order, use
    columns)

ALTERNATIVES
  - Lollipop chart
  - Dot plot
  - Treemap (many categories)

EXAMPLE
Most-used programming languages among survey respondents (% of respondents),
synthetic data.

Run:  python horizontal_bar.py

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
df = pd.DataFrame({
    "language": ["JavaScript", "Python", "SQL", "TypeScript", "Bash/Shell", "Java",
                 "C#", "C++", "Go", "Rust", "Kotlin", "R"],
    "pct": [62, 58, 51, 40, 33, 30, 27, 23, 14, 13, 9, 5],
}).sort_values("pct")
df.tail()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5.5))
bars = ax.barh(df["language"], df["pct"], color=PALETTE[0], height=0.7)
ax.bar_label(bars, fmt="%d%%", padding=4, fontsize=9, color="#52514e")
ax.xaxis.set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.grid(False)
ax.set_title("Languages used by respondents (% of respondents)")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
