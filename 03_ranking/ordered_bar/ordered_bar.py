"""
Ordered Horizontal Bar Chart  -  family: Ranking

DESIGN PURPOSE
Horizontal bars sorted from largest to smallest. Sorting turns comparison into
a ranking that reads top to bottom, and horizontal bars leave room for long
category labels.

WHEN TO USE
  - Rank categories by a single value (top 10 products, countries, causes)
  - Show categories with long names
  - Highlight where one item of interest sits in the ranking

AVOID WHEN
  - The categories have a natural order (months, age bands): keep that order
    instead
  - There are more than ~25 categories (show the top N and fold the rest into
    'Other')

ALTERNATIVES
  - Lollipop chart
  - Cleveland dot plot
  - Ordered column chart

EXAMPLE
Top 12 programming languages by share of developers (synthetic survey),
highlighting Python.

Run:  python ordered_bar.py
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
langs = ["JavaScript", "Python", "SQL", "TypeScript", "Java", "C#", "C++", "Go",
         "Rust", "PHP", "Kotlin", "Swift"]
share = [62.3, 51.0, 48.7, 38.5, 30.1, 27.0, 22.4, 14.2, 13.1, 12.0, 9.4, 5.1]
df = pd.DataFrame({"language": langs, "share_pct": share}).sort_values("share_pct")
df.tail()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 5.5))
colors = [PALETTE[0] if l == "Python" else GRAY for l in df["language"]]
ax.barh(df["language"], df["share_pct"], color=colors, height=0.72)
for y, v in enumerate(df["share_pct"]):
    ax.text(v + 0.8, y, f"{v:.0f}%", va="center", fontsize=9, color="#52514e")
ax.set_xlim(0, 70)
ax.xaxis.set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.grid(False)
ax.set_title("Languages used by developers (% of respondents)")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
