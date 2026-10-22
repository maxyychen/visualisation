"""
Q-Q Plot (Quantile-Quantile)  -  family: Distribution

DESIGN PURPOSE
Plots a sample's quantiles against those of a theoretical distribution,
usually the normal. If the points follow the diagonal, the data fits; curved
tails show skew or heavy tails.

WHEN TO USE
  - Check the normality assumption before t-tests or regression (e.g. on
    residuals)
  - Diagnose skew, heavy tails or outliers relative to a reference
    distribution
  - Compare two samples' distributions quantile by quantile

AVOID WHEN
  - Communicating with a general audience (it is a diagnostic tool)

ALTERNATIVES
  - Histogram with a fitted normal curve
  - ECDF vs. theoretical CDF

EXAMPLE
Normal vs. right-skewed vs. heavy-tailed samples (n = 200 each), side by side.

Run:  python qq_plot.py
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
from scipy import stats
rng = np.random.default_rng(43)
samples = {
    "Normal": rng.normal(0, 1, 200),
    "Right-skewed (lognormal)": rng.lognormal(0, 0.6, 200),
    "Heavy-tailed (t, df=3)": rng.standard_t(3, 200),
}
{k: round(stats.skew(v), 2) for k, v in samples.items()}

# --- Plot --------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(11, 4))
for ax, (name, x) in zip(axes, samples.items()):
    (osm, osr), (slope, intercept, r) = stats.probplot(x, dist="norm")
    ax.scatter(osm, osr, s=14, color=PALETTE[0], alpha=0.7, edgecolor="none")
    ax.plot(osm, slope * osm + intercept, color=PALETTE[1], linewidth=1.5)
    ax.set_title(name, fontsize=11)
    ax.set_xlabel("Theoretical quantiles")
axes[0].set_ylabel("Sample quantiles")
fig.suptitle("Q-Q plots against the normal distribution", x=0.01, ha="left", weight="bold")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
