"""
t-SNE / UMAP Embedding  -  family: Multivariate & ML

DESIGN PURPOSE
A non-linear projection that places observations with similar profiles near
each other in 2-D. It shows local neighbourhoods, clusters and how well
labelled groups separate in high-dimensional data.

WHEN TO USE
  - Explore whether high-dimensional samples (patients, cells, documents) form
    clusters
  - Check whether known labels correspond to natural groupings in the features
  - Present single-cell, omics or embedding-model output

AVOID WHEN
  - You want to read distances or sizes between clusters (t-SNE does not
    preserve them)
  - The axes would be interpreted as variables (they have no meaning)
  - There are few variables, or a linear method such as PCA already shows the
    structure

ALTERNATIVES
  - PCA biplot (linear, interpretable axes)
  - UMAP (umap-learn package; faster, keeps more global structure)
  - Clustered heatmap

EXAMPLE
The real Breast Cancer Wisconsin (Diagnostic) dataset bundled with scikit-
learn (load_breast_cancer). It has 569 tumours, each with 30 cell-nucleus
measurements and a benign/malignant diagnosis.

Run:  python tsne_embedding.py
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

from sklearn.datasets import load_breast_cancer
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

# --- Example data ------------------------------------------------------------
bc = load_breast_cancer(as_frame=True)
Z = StandardScaler().fit_transform(bc.data)
emb = TSNE(n_components=2, perplexity=30, init="pca", random_state=0).fit_transform(Z)
df = pd.DataFrame(emb, columns=["dim1", "dim2"])
df["diagnosis"] = bc.target.map({0: "Malignant", 1: "Benign"})
df["diagnosis"].value_counts()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 6))
for color, label in zip(PALETTE, ["Benign", "Malignant"]):
    g = df[df["diagnosis"] == label]
    ax.scatter(g["dim1"], g["dim2"], s=22, alpha=0.75, color=color,
               edgecolor="#fcfcfb", linewidth=0.5, label=f"{label} (n={len(g)})")
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
ax.set_xlabel("t-SNE 1 (no units)")
ax.set_ylabel("t-SNE 2 (no units)")
ax.set_title("Tumours cluster by diagnosis (t-SNE of 30 features)")
ax.legend(loc="best")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
