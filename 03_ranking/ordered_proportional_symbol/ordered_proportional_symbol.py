"""
Ordered Proportional Symbol Chart  -  family: Ranking

DESIGN PURPOSE
Circles sized by value and arranged in rank order. It suits values that span a
very wide range, where bars for the small items would be too short to see.

WHEN TO USE
  - Rank items whose values differ by orders of magnitude (company valuations,
    city populations)
  - Make an eye-catching infographic where visual impact matters more than
    precision

AVOID WHEN
  - Precise comparison is needed (people underestimate area differences)
  - Values are similar (the circles all look the same)

ALTERNATIVES
  - Ordered bar chart with a log axis
  - Packed bubble chart

EXAMPLE
Market value ($bn) of the 10 largest companies in a fictional stock index;
values span two orders of magnitude.

Run:  python ordered_proportional_symbol.py
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
companies = ["Novacorp", "Helion", "Quanta", "Meridian", "Orbis", "Vantage", "Kestrel",
             "Lumen", "Tessel", "Zephyr"]
value_bn = [2900, 1700, 1100, 640, 420, 260, 150, 90, 55, 30]
df = pd.DataFrame({"company": companies, "value_bn": value_bn}).sort_values("value_bn", ascending=False)
df

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 3.4))
r = np.sqrt(df["value_bn"].values / np.pi)         # area proportional to value
r = r / r.max() * 0.45
gaps = np.maximum(r[:-1] + r[1:] + 0.06, 0.6)      # keep small circles' labels apart
x = np.cumsum(np.r_[r[0], gaps])
for xi, ri, (_, row) in zip(x, r, df.iterrows()):
    ax.add_patch(plt.Circle((xi, 0), ri, color=PALETTE[0], alpha=0.85))
    label = f"{row['value_bn']:,.0f}"
    if ri > 0.15:                                  # value inside big circles, above small ones
        ax.text(xi, 0, label, ha="center", va="center", color="white", fontsize=10, weight="bold")
    else:
        ax.text(xi, ri + 0.04, label, ha="center", va="bottom", color="#0b0b0b", fontsize=9.5, weight="bold")
    ax.text(xi, -0.55, row["company"], ha="center", va="top", fontsize=9, color="#52514e")
ax.set_xlim(-0.05, x[-1] + max(r[-1], 0.3) + 0.05)
ax.set_ylim(-0.8, 0.5)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Largest companies in the index (market value, $bn)")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
