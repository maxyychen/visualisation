"""
Partial Dependence & ICE Plot  -  family: Multivariate & ML

DESIGN PURPOSE
Shows how a model's prediction changes as one feature varies while the others
stay at their observed values. Thin ICE lines trace individual cases and the
bold line is their average (partial dependence), which exposes the shape of a
feature's effect: linear, threshold, plateau or interaction.

WHEN TO USE
  - Explain the shape of a feature's effect in a black-box model (gradient
    boosting, random forest)
  - Check for thresholds or saturation that a linear model would miss
  - Spot interactions (ICE lines that are not parallel)

AVOID WHEN
  - The feature is strongly correlated with others (the model gets evaluated
    on impossible combinations)
  - You need effects for more than ~2 features at once

ALTERNATIVES
  - SHAP dependence plot
  - Accumulated local effects (ALE) plot, which copes better with correlated
    features

EXAMPLE
A gradient-boosting model of disease progression one year after baseline,
fitted to the real Diabetes dataset bundled with scikit-learn (load_diabetes,
442 patients, standardized features). The panels show BMI and the serum
triglycerides measure (s5).

Run:  python partial_dependence.py
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

from sklearn.datasets import load_diabetes
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.inspection import PartialDependenceDisplay

# --- Example data ------------------------------------------------------------
diab = load_diabetes(as_frame=True)
X, y = diab.data, diab.target
model = GradientBoostingRegressor(n_estimators=300, max_depth=2, learning_rate=0.05,
                                  random_state=0).fit(X, y)
print(f"R² on training data: {model.score(X, y):.2f}")
X.describe().loc[["mean", "std"], ["bmi", "s5"]].round(3)

# --- Plot --------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharey=True)
PartialDependenceDisplay.from_estimator(
    model, X, ["bmi", "s5"], kind="both", subsample=80, random_state=0, ax=axes,
    ice_lines_kw={"color": "#b8b7b1", "alpha": 0.35, "linewidth": 0.7},
    pd_line_kw={"color": PALETTE[0], "linewidth": 2.5, "linestyle": "-"})
for ax, name in zip(axes, ["BMI (standardized)", "s5: log serum triglycerides (standardized)"]):
    ax.set_xlabel(name)
    ax.grid(True, color="#e6e5e1", linewidth=0.6)
    leg = ax.get_legend()
    if leg:
        leg.remove()
axes[0].set_ylabel("Predicted disease progression")
axes[1].set_ylabel("")
fig.suptitle("Progression rises sharply above average BMI and triglycerides",
             x=0.02, ha="left", fontsize=13, fontweight="bold")
fig.text(0.02, 0.005, "Gray: individual patients (ICE)   Blue: average effect (partial dependence)",
         fontsize=9, color="#52514e")
fig.tight_layout(rect=(0, 0.03, 1, 1))

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
