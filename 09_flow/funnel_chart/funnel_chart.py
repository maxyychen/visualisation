"""
Funnel Chart  -  family: Flow

DESIGN PURPOSE
A sequence of centered bars, one per stage of a process, each no larger than
the one before. It shows how many items remain at each step and where the
largest drop-offs occur.

WHEN TO USE
  - Show a sales or marketing conversion pipeline (visit → sign-up → purchase)
  - Show applicant screening pipelines (loan applications, hiring, trial
    recruitment)
  - Find the stage with the biggest loss

AVOID WHEN
  - Stages are not strictly sequential or subsets of each other
  - Values can increase between stages (use a bar chart or waterfall)

ALTERNATIVES
  - Horizontal bar chart with conversion %
  - Sankey diagram (to show where drop-offs go)

EXAMPLE
A B2B sales pipeline for one year, from inbound leads to closed-won deals.

Run:  python funnel_chart.py

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
stages = pd.Series({"Leads": 2400, "Qualified": 1150, "Demo held": 640,
                    "Proposal sent": 410, "Closed-won": 230})
stages.to_frame("deals").assign(step_conversion=(stages / stages.shift()).round(2))

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
y = np.arange(len(stages))[::-1]
ax.barh(y, stages.values, left=-stages.values / 2, color=PALETTE[0], height=0.8)
for yi, (name, v), prev in zip(y, stages.items(), [None] + list(stages.values[:-1])):
    ax.text(0, yi, f"{v:,}", ha="center", va="center", color="white", fontweight="bold")
    ax.text(-stages.max() / 2 - 60, yi, name, ha="right", va="center", fontsize=10)
    if prev:
        ax.text(stages.max() / 2 + 60, yi, f"{v / prev:.0%} of previous", ha="left",
                va="center", fontsize=9, color="#52514e")
ax.set_xlim(-stages.max() / 2 - 500, stages.max() / 2 + 500)
ax.axis("off")
ax.set_title(f"Sales pipeline: {stages.iloc[-1] / stages.iloc[0]:.0%} of leads become customers")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
