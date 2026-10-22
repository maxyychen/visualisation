"""
Clustered Heatmap (with dendrograms)  -  family: Scientific & clinical

DESIGN PURPOSE
A matrix heatmap whose rows and columns are reordered by hierarchical
clustering, with dendrograms on the margins. Blocks of similar features and
similar samples emerge without any prior grouping.

WHEN TO USE
  - Show gene expression signatures across samples
  - Group customers, products or sensors by similarity profiles
  - Show a correlation matrix where variable order should reveal clusters

AVOID WHEN
  - There are more than about 200 rows (summarise first or filter to the top-
    variance features)
  - Rows must keep a meaningful fixed order (time, rank)

ALTERNATIVES
  - Plain heatmap
  - PCA / UMAP scatter
  - Parallel coordinates

EXAMPLE
Synthetic expression of 40 genes in 16 samples (8 tumour, 8 normal) containing
two co-regulated modules.

Run:  python clustered_heatmap.py
      python clustered_heatmap.py --real-data   (real dataset: sklearn.datasets.load_breast_cancer() — 40 sampled tumours (20 malignant, 20 benign), 10 nucleus features, bundled with scikit-learn)
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

import seaborn as sns
from matplotlib.patches import Patch

# --- Example data ------------------------------------------------------------
rng = np.random.default_rng(3)
group = np.array(["Tumour"] * 8 + ["Normal"] * 8)
rng.shuffle(group)
expr = rng.normal(0, 1, (40, 16))
is_t = group == "Tumour"
expr[:12, is_t] += 2.2      # module up in tumour
expr[12:22, is_t] -= 1.8    # module down in tumour
expr[22:30] += np.linspace(-1, 1, 16)  # gradient module
genes = [f"G{i:02d}" for i in range(40)]
df = pd.DataFrame(expr + 8, index=genes, columns=[f"S{i:02d}" for i in range(16)])
group_palette = {"Tumour": PALETTE[1], "Normal": PALETTE[0]}
title = "Clustered expression heatmap"
df.iloc[:5, :6]

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # sklearn.datasets.load_breast_cancer() — 40 sampled tumours (20 malignant, 20 benign), 10 nucleus features, bundled with scikit-learn
    from sklearn.datasets import load_breast_cancer
    bc = load_breast_cancer(as_frame=True)
    rng = np.random.default_rng(3)
    target = bc.target.values
    idx = np.r_[rng.choice(np.where(target == 0)[0], 20, replace=False),
                rng.choice(np.where(target == 1)[0], 20, replace=False)]
    rng.shuffle(idx)
    feats = [c for c in bc.feature_names if c.startswith("mean ")]      # 10 nucleus features
    df = bc.data.loc[idx, feats].T
    df.columns = [f"P{i:02d}" for i in range(len(idx))]
    group = np.where(target[idx] == 0, "Malignant", "Benign")
    group_palette = {"Malignant": PALETTE[1], "Benign": PALETTE[0]}
    title = "Breast tumours clustered by nucleus features"
    df.iloc[:5, :6]

# --- Plot --------------------------------------------------------------------
group_colors = pd.Series(group, index=df.columns).map(group_palette)
g = sns.clustermap(df, z_score=0, cmap=DIV_CMAP, center=0, vmin=-2.5, vmax=2.5, method="average",
                   metric="correlation", col_colors=group_colors, figsize=(8, 9),
                   dendrogram_ratio=(0.15, 0.12), cbar_pos=(0.02, 0.84, 0.03, 0.12),
                   yticklabels=True, tree_kws=dict(linewidths=0.8, colors="#52514e"))
g.ax_heatmap.tick_params(axis="y", labelsize=7)
g.ax_cbar.set_title("z-score", fontsize=9)
g.ax_heatmap.legend(handles=[Patch(color=c, label=k) for k, c in group_palette.items()],
                    loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=2)
g.figure.suptitle(title, x=0.55, y=1.01, fontweight="bold")
fig = g.figure

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
