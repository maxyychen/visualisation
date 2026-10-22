"""
Unsorted Rainbow Bars vs. Sorted Bars  -  family: Bad vs. good

DESIGN PURPOSE
Bars in alphabetical (or random) order, each in a different color, make the
reader do the sorting in their head. The colors carry no information but
suggest that they do, and vertical bars with long names force rotated, hard-
to-read labels.

WHEN TO USE
  - Sort nominal categories by value so ranking is immediate
  - Use horizontal bars when category names are long
  - Use one color for one series; add a second color only to highlight

AVOID WHEN
  - Alphabetical ordering of categories that have no natural order
  - Coloring each bar differently "to look nice"
  - Rotated 45°/90° x-axis labels

ALTERNATIVES
  - Sorted horizontal bar chart
  - Lollipop or Cleveland dot plot for many categories

EXAMPLE
Average outpatient waiting time (minutes) for ten clinics.

Run:  python unsorted_bars.py
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
rng = np.random.default_rng(4)
clinics = ["Cardiology", "Dermatology", "Endocrinology", "Gastroenterology", "Hematology",
           "Nephrology", "Neurology", "Oncology", "Orthopedics", "Pulmonology"]
df = pd.DataFrame({"clinic": clinics, "wait_min": rng.uniform(12, 45, len(clinics)).round(0)})
TARGET = 30
df

# --- Plot --------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Misleading: alphabetical, rainbow, rotated labels.
ax1.bar(df["clinic"], df["wait_min"], color=plt.get_cmap("rainbow")(np.linspace(0, 1, len(df))))
ax1.tick_params(axis="x", rotation=60)
ax1.set_ylabel("Average wait (min)")
ax1.set_title("✗ Misleading: alphabetical, rainbow, tilted labels", fontsize=11.5)

# Better: sorted, horizontal, one color + highlight for "over target".
d = df.sort_values("wait_min")
colors = np.where(d["wait_min"] > TARGET, PALETTE[1], GRAY)
ax2.barh(d["clinic"], d["wait_min"], color=colors, height=0.7)
ax2.axvline(TARGET, color="#52514e", linewidth=1)
ax2.text(TARGET + 0.5, -0.9, f"{TARGET}-min target", fontsize=9, color="#52514e", va="center")
ax2.set_ylim(-1.3, len(d) - 0.4)
for y, v in enumerate(d["wait_min"]):
    ax2.text(v + (1.6 if abs(v - TARGET) < 2 else 0.6), y, f"{v:.0f}", va="center", fontsize=9, color="#52514e")
ax2.set_xlabel("Average wait (min)")
ax2.set_xlim(0, d["wait_min"].max() * 1.15)
ax2.grid(axis="y", visible=False)
ax2.set_title("✓ Better: sorted, horizontal, color = over target", fontsize=11.5)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
