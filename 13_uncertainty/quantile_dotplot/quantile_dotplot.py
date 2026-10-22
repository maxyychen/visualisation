"""
Quantile Dotplot  -  family: Uncertainty

DESIGN PURPOSE
Turns a probability distribution into a small number of dots (here 20), each
holding an equal share of probability (5%), stacked like a histogram. Readers
can count dots to answer "what are my chances?" without reading a density
curve. Kay et al. (2016) showed people make better decisions with it than with
densities or intervals.

WHEN TO USE
  - Communicate a predictive distribution to the public (arrival times,
    waiting times, forecasts)
  - Support a threshold decision ("how likely is it before 10 minutes?")
  - Show risk as frequencies, which most people find easier than percentages

AVOID WHEN
  - You need fine detail in the tails (20–50 dots cannot show rare events)
  - Comparing many distributions at once (use half-eye or gradient intervals)

ALTERNATIVES
  - Icon array (for a single probability)
  - Half-eye plot
  - CDF / ECDF plot (exact cumulative probabilities)

REFERENCE
  - Kay, M., Kola, T., Hullman, J. R. & Munson, S. A. (2016). When (ish) is my
    bus? User-centered visualizations of uncertainty in everyday, mobile
    predictive systems. Proceedings of the ACM CHI Conference on Human Factors
    in Computing Systems (CHI 2016). https://idl.uw.edu/papers/when-ish-is-my-
    bus

EXAMPLE
A predicted bus arrival time, modelled as a log-normal distribution with a
median of about 11 minutes (after the "When (ish) is my bus?" study, Kay et
al., CHI 2016).

Run:  python quantile_dotplot.py
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

from matplotlib.patches import Circle
from scipy import stats

# --- Example data ------------------------------------------------------------
n_dots = 20
dist = stats.lognorm(s=0.35, scale=11)          # median ~11 minutes
q = dist.ppf((np.arange(n_dots) + 0.5) / n_dots)  # one dot per 5% of probability
threshold = 9
df = pd.DataFrame({"minutes": q.round(1), "bin": np.round(q).astype(int)})
print(f"P(arrival ≤ {threshold} min) ≈ {dist.cdf(threshold + 0.5):.0%}")
df.T

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 3.8))
r = 0.45
counts = {}
for b in df["bin"]:
    k = counts.get(b, 0)
    counts[b] = k + 1
    color = PALETTE[0] if b <= threshold else "#b8b7b1"
    ax.add_patch(Circle((b, r + 2 * r * k + 0.02), r, color=color, linewidth=0))
n_before = int((df["bin"] <= threshold).sum())
ax.axvline(threshold + 0.5, color="#52514e", lw=1)
ax.text(threshold + 0.6, 4.6, f"{n_before} of {n_dots} dots\n≈ {n_before / n_dots:.0%} chance\nby {threshold} min",
        fontsize=9.5, color="#0b0b0b", va="top")
ax.set_xlim(df["bin"].min() - 2, df["bin"].max() + 2)
ax.set_ylim(0, 5)
ax.set_aspect("equal")
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.grid(False)
ax.set_xticks(range(df["bin"].min() - 1, df["bin"].max() + 2, 2))
ax.set_xlabel("Minutes until the bus arrives (each dot = 5% chance)")
ax.set_title("When will my bus arrive?")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
