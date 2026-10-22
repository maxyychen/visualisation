"""
Spaghetti Chart vs. Highlight  -  family: Bad vs. good

DESIGN PURPOSE
Plotting a dozen or more colored lines together produces a "spaghetti" tangle.
Colors run out and repeat, the legend becomes a lookup puzzle, and no single
story stands out. The reader cannot follow any one line.

WHEN TO USE
  - Highlight the one or two series that carry the message and gray the rest
    as context
  - Use small multiples when every series matters equally

AVOID WHEN
  - More than ~4–5 series on one line chart, each with its own color
  - Default color cycles that repeat hues after 8–10 series

ALTERNATIVES
  - Highlight one series, gray the rest (with direct labels)
  - Small multiples with the other series as a gray background
  - Interactive chart with hover-to-highlight

EXAMPLE
Hospital readmission rate (%) for 12 regions, 2014–2024.

Run:  python spaghetti_vs_highlight.py
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
rng = np.random.default_rng(8)
years = np.arange(2014, 2025)
series = {}
for i in range(12):
    base = rng.uniform(13, 17) + np.cumsum(rng.normal(0, 0.35, len(years)))
    series[f"Region {i + 1}"] = base
series["Region 7"] = 16 - 0.55 * (years - 2014) + rng.normal(0, 0.2, len(years))
df = pd.DataFrame(series, index=years)
df.round(1).head()

# --- Plot --------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)

# Misleading: 12 colors, a legend, no focus.
cmap = plt.get_cmap("tab10")
for i, col in enumerate(df.columns):
    ax1.plot(df.index, df[col], color=cmap(i % 10), linewidth=1.6, label=col)
ax1.legend(ncol=2, fontsize=7.5, loc="lower left")
ax1.set_ylabel("Readmission rate (%)")
ax1.set_title("✗ Misleading: 12 colored lines — who improved?", fontsize=11.5)

# Better: gray context, one highlight, the median for reference, direct labels.
for col in df.columns:
    ax2.plot(df.index, df[col], color=GRAY, linewidth=1, alpha=0.7)
med = df.drop(columns="Region 7").median(axis=1)
ax2.plot(df.index, med, color="#52514e", linewidth=1.8)
ax2.plot(df.index, df["Region 7"], color=PALETTE[0], linewidth=2.5)
ax2.text(years[-1] + 0.2, df["Region 7"].iloc[-1], "Region 7", color=PALETTE[0],
         va="center", fontsize=10, fontweight="bold")
ax2.text(years[-1] + 0.2, med.iloc[-1], "Median of\nother regions", color="#52514e",
         va="center", fontsize=9)
ax2.set_xlim(years[0], years[-1] + 2.2)
ax2.set_title("✓ Better: Region 7 cut readmissions; others flat", fontsize=11.5)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
