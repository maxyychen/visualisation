"""
Diverging Column (over time)  -  family: Deviation

DESIGN PURPOSE
Vertical bars rising from or falling below zero, one per time period. Each
discrete period's positive or negative result stands on its own.

WHEN TO USE
  - Show discrete periods with signed results (monthly net cash flow,
    quarterly earnings surprise)
  - Count the positive and negative periods

AVOID WHEN
  - The data is continuous and dense (use a surplus/deficit line)
  - There are more than ~60 periods

ALTERNATIVES
  - Surplus/deficit filled line
  - Waterfall chart (to show the cumulative effect)

EXAMPLE
Monthly net cash flow of a small business over two years, simulated data.

Run:  python diverging_column_time.py
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
rng = np.random.default_rng(5)
months = pd.period_range("2023-01", periods=24, freq="M")
df = pd.DataFrame({"month": months.strftime("%b %y"),
                   "net_cash_k": (rng.normal(4, 12, 24)).round(1)})
df.head()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.5))
colors = np.where(df["net_cash_k"] >= 0, PALETTE[0], PALETTE[1])
ax.bar(df["month"], df["net_cash_k"], color=colors, width=0.75)
ax.axhline(0, color="#52514e", linewidth=1)
ax.set_ylabel("Net cash flow ($k)")
ax.set_title("Monthly net cash flow")
ax.tick_params(axis="x", rotation=60)
ax.grid(axis="x", visible=False)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
