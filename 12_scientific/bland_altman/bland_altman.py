"""
Bland–Altman Plot  -  family: Scientific

DESIGN PURPOSE
Plots the difference between two measurement methods against their mean, with
lines for the mean bias and the 95% limits of agreement. It answers whether
two methods agree well enough to be interchangeable, which a correlation
coefficient cannot.

WHEN TO USE
  - Compare a new measurement device or assay with a reference standard
  - Assess inter-rater or test–retest agreement on a continuous scale
  - Detect proportional bias, where the difference grows with magnitude

AVOID WHEN
  - Measurements are categorical (use Cohen's kappa or a confusion matrix)
  - The goal is prediction rather than agreement (use a scatter plot with
    regression)

ALTERNATIVES
  - Scatter plot with identity line
  - Passing–Bablok / Deming regression plot

EXAMPLE
Simulated systolic blood pressure measured in 150 patients with a cuff device
(A) and an arterial line (B).

Run:  python bland_altman.py
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
rng = np.random.default_rng(9)
true_sbp = rng.normal(128, 18, 150)
method_a = true_sbp + rng.normal(0, 4, 150)
method_b = true_sbp + 3 + 0.06 * (true_sbp - 128) + rng.normal(0, 5, 150)
df = pd.DataFrame({"cuff": method_a.round(1), "arterial": method_b.round(1)})
df["mean"] = (df.cuff + df.arterial) / 2
df["diff"] = df.arterial - df.cuff
bias, sd = df["diff"].mean(), df["diff"].std(ddof=1)
loa = (bias - 1.96 * sd, bias + 1.96 * sd)
print(f"bias = {bias:.2f} mmHg, limits of agreement = {loa[0]:.2f} to {loa[1]:.2f}")
df.head()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.scatter(df["mean"], df["diff"], s=28, color=PALETTE[0], alpha=0.75,
           edgecolor="#fcfcfb", linewidth=0.8)
ax.axhline(0, color=GRAY, linewidth=1)
ax.axhline(bias, color="#0b0b0b", linewidth=1.2)
for v in loa:
    ax.axhline(v, color=PALETTE[1], linewidth=1.2)
x_lab = df["mean"].max() + 2
for v, lab in [(bias, f"Mean bias {bias:+.1f}"), (loa[1], f"+1.96 SD {loa[1]:+.1f}"),
               (loa[0], f"−1.96 SD {loa[0]:+.1f}")]:
    ax.text(x_lab, v + 0.3, lab, va="bottom", fontsize=9, color="#0b0b0b")
ax.set_xlim(df["mean"].min() - 3, df["mean"].max() + 22)
ax.set_xlabel("Mean of the two methods (mmHg)")
ax.set_ylabel("Arterial − cuff (mmHg)")
ax.set_title("Bland–Altman: arterial line vs. cuff systolic BP")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
