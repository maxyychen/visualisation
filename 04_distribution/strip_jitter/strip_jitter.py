"""
Strip Plot (Jittered Dots)  -  family: Distribution

DESIGN PURPOSE
Plots every observation as a dot along a value axis, with random sideways
jitter to reduce overlap. Nothing is summarised away, so sample size, clusters
and outliers stay visible.

WHEN TO USE
  - Show small to medium samples (under ~300 per group) where every point
    matters
  - Expose the raw data behind a summary statistic
  - Overlay on box or violin plots

AVOID WHEN
  - Samples are large (dots merge into a blob)

ALTERNATIVES
  - Beeswarm plot
  - Box plot with points
  - Raincloud plot

EXAMPLE
Sales uplift (%) per store in a three-arm promotion test, 40 stores per arm,
with group means.

Run:  python strip_jitter.py
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
rng = np.random.default_rng(19)
arms = {"No promotion": (1, 4), "10% discount": (7, 5), "Buy 2 get 1": (11, 6)}
df = pd.concat([pd.DataFrame({"arm": a, "shrink_pct": rng.normal(m, s, 40)})
                for a, (m, s) in arms.items()], ignore_index=True)
df.groupby("arm")["shrink_pct"].agg(["mean", "std", "count"]).round(1)

# --- Plot --------------------------------------------------------------------
import seaborn as sns
fig, ax = plt.subplots(figsize=(7, 5))
sns.stripplot(data=df, x="arm", y="shrink_pct", hue="arm", palette=PALETTE[:3], legend=False,
              jitter=0.22, size=6, alpha=0.75, edgecolor="#fcfcfb", linewidth=0.6, ax=ax)
means = df.groupby("arm", sort=False)["shrink_pct"].mean()
for i, m in enumerate(means):
    ax.hlines(m, i - 0.32, i + 0.32, color="#0b0b0b", linewidth=2.2, zorder=4)
    ax.text(i + 0.36, m, f"{m:.0f}%", va="center", fontsize=9)
ax.axhline(0, color="#52514e", linewidth=0.8)
ax.set_xlabel(None)
ax.set_ylabel("Sales uplift vs. last year (%)")
ax.set_title("Sales uplift by promotion (n = 40 stores each)")
ax.grid(axis="x", visible=False)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
