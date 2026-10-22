"""
Density Plot (KDE)  -  family: Distribution

DESIGN PURPOSE
A smoothed, continuous estimate of a distribution (kernel density estimate).
With no bin edges it shows shape clearly, and two or three groups can overlay
without the clutter of overlapping bars.

WHEN TO USE
  - Compare the shapes of two or three distributions on one axis
  - Show a smooth shape when the bin choice would distract

AVOID WHEN
  - The sample is small (the smoothing invents shape)
  - The data is bounded (e.g. ≥ 0) and the curve would spill past the bound
  - The audience is unfamiliar with density (the y-axis is not a count)

ALTERNATIVES
  - Histogram
  - Ridgeline plot
  - Violin plot

EXAMPLE
Exam scores of three classes taught with different methods (synthetic).

Run:  python kde_density.py
      python kde_density.py --real-data   (real dataset: plotly.express.data.iris() — Fisher's (1936) iris measurements, bundled with plotly)

The notebook also shows this chart built with: altair.
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
rng = np.random.default_rng(14)
df = pd.concat([
    pd.DataFrame({"score": rng.normal(68, 9, 300), "method": "Lecture"}),
    pd.DataFrame({"score": rng.normal(74, 7, 300), "method": "Flipped"}),
    pd.DataFrame({"score": np.r_[rng.normal(60, 6, 150), rng.normal(82, 6, 150)],
                  "method": "Self-paced"}),
], ignore_index=True)
x, hue, order = "score", "method", ["Lecture", "Flipped", "Self-paced"]
labels = dict(x="Exam score", title="Exam score distribution by teaching method")
df.groupby(hue)[x].describe().round(1)

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.iris() — Fisher's (1936) iris measurements, bundled with plotly
    import plotly.express as px
    df = px.data.iris()
    x, hue, order = "sepal_length", "species", ["setosa", "versicolor", "virginica"]
    labels = dict(x="Sepal length (cm)", title="Sepal length by iris species (Fisher, 1936)")
    df.groupby(hue)[x].describe().round(1)

# --- Plot --------------------------------------------------------------------
import seaborn as sns
fig, ax = plt.subplots(figsize=(8, 4.8))
sns.kdeplot(data=df, x=x, hue=hue, hue_order=order,
            palette=PALETTE[:len(order)], fill=True, alpha=0.2, linewidth=2, common_norm=False, ax=ax)
ax.set_xlabel(labels["x"])
ax.set_ylabel("Density")
ax.set_title(labels["title"])
ax.get_legend().set_title(None)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
