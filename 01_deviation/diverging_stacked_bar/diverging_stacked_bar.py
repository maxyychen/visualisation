"""
Diverging Stacked Bar (Likert)  -  family: Deviation

DESIGN PURPOSE
Stacks survey response levels so negative answers extend left and positive
answers extend right from a central neutral line. Overall sentiment and its
composition show together.

WHEN TO USE
  - Show Likert-scale survey results (disagree ↔ agree)
  - Compare sentiment across many questions or groups at a glance
  - Show ordered categorical responses that have a natural midpoint

AVOID WHEN
  - Responses are not ordered or have no natural neutral point
  - Readers need exact values for the inner segments (use a table)
  - There are more than 5–7 response levels

ALTERNATIVES
  - 100% stacked bar
  - Small-multiple bar charts per question

EXAMPLE
Employee engagement survey with five questions on a 5-point agreement scale.

Run:  python diverging_stacked_bar.py
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
levels = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
questions = ["I feel valued", "Workload is manageable", "Clear career path",
             "Good team communication", "Would recommend employer"]
pct = np.array([[5, 12, 20, 40, 23],
                [14, 26, 22, 28, 10],
                [18, 30, 25, 19, 8],
                [3, 8, 15, 45, 29],
                [6, 14, 24, 35, 21]], dtype=float)
df = pd.DataFrame(pct, index=questions, columns=levels)
df = df.loc[(df["Agree"] + df["Strongly agree"]).sort_values().index]
df

# --- Plot --------------------------------------------------------------------
colors = ["#c4462b", "#f0a07f", "#d0cfca", "#86b6ef", "#1c5cab"]
left_start = -(df.iloc[:, 0] + df.iloc[:, 1] + df.iloc[:, 2] / 2)
fig, ax = plt.subplots(figsize=(9, 4.5))
left = left_start.values.copy()
for level, color in zip(df.columns, colors):
    ax.barh(df.index, df[level], left=left, color=color, label=level,
            height=0.65, edgecolor="#fcfcfb", linewidth=1.5)
    left += df[level].values
ax.axvline(0, color="#52514e", linewidth=1)
ax.set_xlim(-70, 85)
ax.set_xticks(range(-60, 81, 20))
ax.set_xticklabels([f"{abs(t)}%" for t in range(-60, 81, 20)])
ax.grid(axis="y", visible=False)
ax.set_title("Employee engagement survey")
ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.45, -0.1), fontsize=8.5)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
