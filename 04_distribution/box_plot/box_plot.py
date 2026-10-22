"""
Box Plot (Box-and-Whisker)  -  family: Distribution

DESIGN PURPOSE
Summarises a distribution with five numbers: the median, the quartiles (box)
and the whiskers to 1.5×IQR, with outliers drawn as points. It is compact
enough to compare many groups side by side.

WHEN TO USE
  - Compare the medians and spreads of many groups
  - Flag outliers
  - Fit a statistical audience and small spaces

AVOID WHEN
  - The distribution is multimodal (the box hides the peaks; use a violin or
    raincloud)
  - Sample sizes are small (show the points instead)
  - The audience is unfamiliar with quartiles

ALTERNATIVES
  - Violin plot
  - Raincloud plot
  - Strip plot

EXAMPLE
Days taken to pay an invoice, by customer segment, for 1,000 invoices
(synthetic).

Run:  python box_plot.py

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
rng = np.random.default_rng(6)
segments = {"Card on file": (1.0, 0.5), "Small business": (2.9, 0.35), "Retail chain": (3.3, 0.3),
            "Enterprise": (3.6, 0.35), "Distributor": (3.5, 0.5), "Government": (3.9, 0.55)}
df = pd.concat([pd.DataFrame({"segment": d, "days_to_pay": rng.lognormal(mu, sd, 170)})
                for d, (mu, sd) in segments.items()], ignore_index=True)
order = df.groupby("segment")["days_to_pay"].median().sort_values().index.tolist()
df.groupby("segment")["days_to_pay"].median().round(1)

# --- Plot --------------------------------------------------------------------
import seaborn as sns
fig, ax = plt.subplots(figsize=(8.5, 5))
sns.boxplot(data=df, x="segment", y="days_to_pay", order=order, color=PALETTE[0], width=0.55,
            boxprops=dict(alpha=0.35), linewidth=1.2,
            flierprops=dict(marker="o", markersize=3, markerfacecolor="#52514e",
                            markeredgecolor="none", alpha=0.5),
            medianprops=dict(color="#0b0b0b", linewidth=2), ax=ax)
ax.set_yscale("log")
ax.set_yticks([1, 2, 5, 10, 30, 60, 120, 240], ["1", "2", "5", "10", "30", "60", "120", "240"])
ax.set_xlabel(None)
ax.set_ylabel("Days to pay (log scale)")
ax.set_title("Days to pay an invoice, by customer segment")
ax.grid(axis="x", visible=False)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
