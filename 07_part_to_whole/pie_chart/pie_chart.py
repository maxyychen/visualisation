"""
Pie Chart  -  family: Part-to-whole

DESIGN PURPOSE
A circle divided into slices that add up to 100%. It answers one question:
roughly what share of the whole is each part? People judge angles and areas
less accurately than lengths, so a pie is for a rough picture, not precise
comparison.

WHEN TO USE
  - Show a simple part-to-whole split with few slices (≤ 6, ideally 2–4)
  - Show that one part is clearly dominant (about half or more)
  - General-audience communication where the 'slices of a whole' metaphor
    helps

AVOID WHEN
  - There are more than 6 slices (fold the small ones into 'Other' or use a
    bar chart)
  - Slices are close in size and the difference matters
  - Comparing several pies side by side (use a 100% stacked bar)
  - The parts don't add up to a meaningful whole
  - 3-D or exploded pies, which distort the angles

ALTERNATIVES
  - Bar chart
  - Donut chart
  - Waffle chart
  - 100% stacked bar

EXAMPLE
Share of web traffic by source (illustrative); seven sources, the three
smallest folded into 'Other' to keep 5 slices.

Run:  python pie_chart.py

The notebook also shows this chart built with: plotly.
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
raw = pd.Series({"Organic search": 41, "Direct": 24, "Social": 14, "Referral": 11,
                 "Email": 6, "Paid": 2.5, "Affiliates": 1.5})
# Keep at most 5 named slices; fold the tail into "Other"
top = raw.nlargest(4)
s = pd.concat([top, pd.Series({"Other": raw.drop(top.index).sum()})])
s

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 6.5))
colors = PALETTE[:len(s) - 1] + [GRAY]
wedges, _ = ax.pie(s.values, colors=colors, startangle=90, counterclock=False,
                   wedgeprops=dict(edgecolor="#fcfcfb", linewidth=2))
for w, (name, v) in zip(wedges, s.items()):
    ang = np.deg2rad((w.theta1 + w.theta2) / 2)
    x, y = np.cos(ang), np.sin(ang)
    ax.annotate(f"{name}\n{v:.0f}%", xy=(0.98 * x, 0.98 * y), xytext=(1.25 * x, 1.2 * y),
                ha="center", va="center", fontsize=10,
                arrowprops=dict(arrowstyle="-", color="#b8b7b1", linewidth=0.8))
ax.set_title("Website traffic by source")
ax.axis("equal")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
