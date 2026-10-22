"""
Spaghetti Plot (Longitudinal Trajectories)  -  family: Healthcare & life sciences

DESIGN PURPOSE
Draws one thin line per subject for repeated measurements over time, with the
group mean and its confidence band on top. Individual variation, dropout and
the average trend are visible together, which a plot of means alone hides.

WHEN TO USE
  - Show repeated lab values, vital signs or scores per patient over follow-up
    visits
  - Show between-patient heterogeneity around an average trajectory
  - Spot unusual individual trajectories, dropout and irregular visit timing

AVOID WHEN
  - There are hundreds of subjects so the lines become a solid mass (sample
    them, use a density band, or facet by group)
  - Only group averages matter and individual data cannot be shown (for
    privacy reasons)

ALTERNATIVES
  - Mean ± CI line chart
  - Small multiples (one panel per patient for small n)
  - Heatmap (patients × visits)

EXAMPLE
eGFR (kidney function) measured at scheduled visits over 24 months in 40
synthetic patients per arm, with some missed visits and dropout. Placebo is
compared with an active treatment.

NOTE: Examples use simulated data. De-identify patient data before analysing
it in notebooks: executed notebooks store their outputs.

Run:  python spaghetti_longitudinal.py
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
rng = np.random.default_rng(12)
visits = np.array([0, 3, 6, 9, 12, 18, 24])
rows = []
for arm, slope_mu in [("Placebo", -0.55), ("Treatment", -0.12)]:
    for i in range(40):
        pid = f"{arm[0]}{i:02d}"
        base = rng.normal(62, 9)
        slope = rng.normal(slope_mu, 0.25)
        if arm == "Treatment" and i == 7:
            slope = -0.9                                     # an atypical decliner to highlight
        last = rng.choice([12, 18, 24, 24, 24, 24])          # dropout
        for v in visits[visits <= last]:
            if v > 0 and rng.random() < 0.08:                # missed visit
                continue
            month = v + rng.normal(0, 0.4) if v else 0
            rows.append({"arm": arm, "patient": pid, "month": month, "visit": v,
                         "egfr": base + slope * month + rng.normal(0, 2.5)})
df = pd.DataFrame(rows)
df.head()

# --- Plot --------------------------------------------------------------------
highlight = "T07"
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True)
for ax, (arm, g) in zip(axes, df.groupby("arm")):
    for pid, p in g.groupby("patient"):
        if pid != highlight:
            ax.plot(p["month"], p["egfr"], color=GRAY, linewidth=0.8, alpha=0.7)
    summary = g.groupby("visit")["egfr"].agg(["mean", "std", "count"])
    ci = 1.96 * summary["std"] / np.sqrt(summary["count"])
    ax.fill_between(summary.index, summary["mean"] - ci, summary["mean"] + ci, color=PALETTE[0], alpha=0.2, linewidth=0)
    ax.plot(summary.index, summary["mean"], color=PALETTE[0], linewidth=3, marker="o", markersize=5,
            markeredgecolor="#fcfcfb", markeredgewidth=1.2)
    ax.text(24.4, summary["mean"].iloc[-1], f"Mean\n{summary['mean'].iloc[-1]:.0f}", color="#0b0b0b",
            fontsize=9, va="center", fontweight="bold")
    if highlight in set(g["patient"]):
        p = g[g["patient"] == highlight]
        ax.plot(p["month"], p["egfr"], color=PALETTE[1], linewidth=2)
        ax.text(p["month"].iloc[-1] + 0.4, p["egfr"].iloc[-1], f"Patient {highlight}", color="#0b0b0b",
                fontsize=9, va="center")
    ax.set_title(f"{arm} (n = {g['patient'].nunique()})")
    ax.set_xticks(visits)
    ax.set_xlim(-0.5, 28.5)
    ax.set_xlabel("Months since baseline")
axes[0].set_ylabel("eGFR (mL/min/1.73 m²)")
fig.suptitle("Kidney function trajectories: individuals (gray) and arm mean ± 95% CI (blue)",
             x=0.01, ha="left", fontsize=13, fontweight="bold")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
