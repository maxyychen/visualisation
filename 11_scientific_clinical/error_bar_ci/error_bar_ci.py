"""
Means with 95% Confidence Intervals  -  family: Scientific & clinical

DESIGN PURPOSE
Plots each group's mean as a dot with a 95% confidence interval, over the raw
observations. Readers see the estimate, its uncertainty, and the data behind
it, which a bar-of-means ('dynamite plot') hides.

WHEN TO USE
  - Compare group means from experiments or trials (dose groups, conditions)
  - Show estimates together with their uncertainty
  - Replace 'dynamite plots' (bars with error whiskers)

AVOID WHEN
  - Distributions are strongly skewed or multimodal (show box, violin or
    raincloud plots)
  - The audience may confuse SD, SE and CI (always say which one in the axis
    label or caption)

ALTERNATIVES
  - Box plot
  - Raincloud plot
  - Forest plot

EXAMPLE
LDL cholesterol reduction after 12 weeks in four dose groups of a synthetic
trial.

Run:  python error_bar_ci.py
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

from scipy import stats

# --- Example data ------------------------------------------------------------
rng = np.random.default_rng(6)
groups = ["Placebo", "10 mg", "20 mg", "40 mg"]
true_mean = [3, 18, 27, 33]
df = pd.concat([pd.DataFrame({"group": g, "ldl_reduction_pct": rng.normal(m, 11, rng.integers(22, 30))})
                for g, m in zip(groups, true_mean)], ignore_index=True)
summary = df.groupby("group", sort=False)["ldl_reduction_pct"].agg(["mean", "std", "count"])
summary["ci95"] = stats.t.ppf(0.975, summary["count"] - 1) * summary["std"] / np.sqrt(summary["count"])
summary.round(2)

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 5))
for i, g in enumerate(groups):
    vals = df.loc[df.group == g, "ldl_reduction_pct"]
    ax.scatter(i + rng.uniform(-0.18, 0.18, len(vals)), vals, s=14, color=GRAY, alpha=0.6, linewidth=0)
ax.errorbar(range(len(groups)), summary["mean"], yerr=summary["ci95"], fmt="o", color=PALETTE[0],
            markersize=9, capsize=6, elinewidth=2, capthick=2, markeredgecolor="#fcfcfb", zorder=3)
for i, (m, n) in enumerate(zip(summary["mean"], summary["count"])):
    ax.text(i + 0.25, m, f"{m:.1f}%", va="center", fontsize=9, color="#0b0b0b")
ax.set_xticks(range(len(groups)), [f"{g}\n(n={n})" for g, n in zip(groups, summary["count"])])
ax.axhline(0, color="#52514e", linewidth=0.8)
ax.grid(axis="x", visible=False)
ax.set_ylabel("LDL reduction at week 12 (%)")
ax.set_title("Mean LDL reduction by dose (dot = mean, bar = 95% CI)")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
