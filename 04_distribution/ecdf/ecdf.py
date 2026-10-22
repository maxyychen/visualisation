"""
Empirical CDF (ECDF)  -  family: Distribution

DESIGN PURPOSE
For every value x, plots the fraction of observations ≤ x. It has no bins or
smoothing, and it answers percentile questions directly ('what share of users
wait under 2 s?').

WHEN TO USE
  - Compare distributions precisely, with no binning choices
  - Read percentiles and thresholds (SLAs, latency, dose response)
  - Overlay several groups without the clutter of overlapping histograms

AVOID WHEN
  - The audience is unfamiliar with cumulative plots (shape is less intuitive
    than a histogram)

ALTERNATIVES
  - Histogram
  - KDE density
  - Box plot

EXAMPLE
Page-load latency for two server versions, 3,000 requests each, with p50 and
p95 marked.

Run:  python ecdf.py

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
rng = np.random.default_rng(29)
df = pd.concat([
    pd.DataFrame({"version": "v1", "latency_ms": rng.lognormal(5.6, 0.45, 3000)}),
    pd.DataFrame({"version": "v2", "latency_ms": rng.lognormal(5.35, 0.35, 3000)}),
], ignore_index=True)
df.groupby("version")["latency_ms"].quantile([0.5, 0.95]).unstack().round(0)

# --- Plot --------------------------------------------------------------------
import seaborn as sns
fig, ax = plt.subplots(figsize=(8, 4.8))
sns.ecdfplot(data=df, x="latency_ms", hue="version", palette=PALETTE[:2], linewidth=2, ax=ax)
for q in [0.5, 0.95]:
    ax.axhline(q, color="#52514e", linewidth=0.8)
    ax.text(1450, q + 0.015, f"p{int(q * 100)}", fontsize=9, color="#52514e", ha="right")
ax.set_xlim(0, 1500)
ax.set_xlabel("Page-load latency (ms)")
ax.set_ylabel("Share of requests ≤ x")
ax.set_title("Latency distribution: v2 is faster across the board")
ax.get_legend().set_title(None)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
