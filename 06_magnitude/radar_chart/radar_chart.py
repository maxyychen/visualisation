"""
Radar (Spider) Chart  -  family: Magnitude

DESIGN PURPOSE
Plots several variables on axes radiating from a center and joins them into a
polygon. Each entity's overall profile reads as a shape.

WHEN TO USE
  - Compare the profile of 1–3 entities across 4–8 variables on the same scale
    (skills, product attributes)
  - Show balance and strengths or weaknesses more than precise values

AVOID WHEN
  - Variables use different units or scales (normalise first, or use a
    different chart)
  - Comparing more than ~3 entities (polygons overlap; use small multiples or
    parallel coordinates)
  - Precise comparison is required (radial distances and areas are hard to
    judge)

ALTERNATIVES
  - Grouped bar chart
  - Parallel coordinates
  - Dot plot

EXAMPLE
Player ratings (0–100) on six skills for two fictional football players.

Run:  python radar_chart.py
      python radar_chart.py --real-data   (real dataset: sklearn.datasets.load_wine() — chemical analysis of 178 Italian wines from 3 cultivars, bundled with scikit-learn)
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
skills = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical"]
df = pd.DataFrame({"Player A": [88, 85, 72, 86, 38, 70],
                   "Player B": [70, 62, 88, 79, 76, 82]}, index=skills)
title = "Player skill profiles"
df

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # sklearn.datasets.load_wine() — chemical analysis of 178 Italian wines from 3 cultivars, bundled with scikit-learn
    from sklearn.datasets import load_wine
    w = load_wine(as_frame=True).frame
    feats = {"alcohol": "Alcohol", "malic_acid": "Malic acid", "flavanoids": "Flavanoids",
             "color_intensity": "Colour intensity", "hue": "Hue", "proline": "Proline"}
    means = w.groupby("target")[list(feats)].mean().rename(columns=feats)
    df = (means / means.max() * 100).T.round(0)          # % of the highest cultivar mean
    df.columns = [f"Cultivar {i + 1}" for i in df.columns]
    title = "Wine cultivars (% of highest mean)"
    df

# --- Plot --------------------------------------------------------------------
angles = np.linspace(0, 2 * np.pi, len(df), endpoint=False).tolist()
angles += angles[:1]
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
for i, col in enumerate(df.columns):
    vals = df[col].tolist() + df[col].tolist()[:1]
    ax.plot(angles, vals, color=PALETTE[i], linewidth=2, label=col)
    ax.fill(angles, vals, color=PALETTE[i], alpha=0.15)
ax.set_xticks(angles[:-1], df.index)
ax.set_ylim(0, 100)
ax.set_yticks([25, 50, 75, 100], ["25", "50", "75", "100"], color="#8c8b86", fontsize=8)
ax.spines["polar"].set_color("#c9c8c3")
ax.set_title(title, pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.08))
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
