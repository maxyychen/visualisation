"""
Precision–Recall Curve  -  family: Scientific & clinical

DESIGN PURPOSE
Plots precision (positive predictive value) against recall (sensitivity)
across thresholds. Unlike ROC, it focuses on the positive class, so it stays
honest when positives are rare.

WHEN TO USE
  - Evaluate classifiers on imbalanced data (rare disease screening, fraud,
    defects)
  - Show the cost of false positives when chasing more recall

AVOID WHEN
  - Classes are balanced and both matter equally (ROC is more familiar)
  - Comparing PR curves across datasets with different prevalence (the
    baselines differ)

ALTERNATIVES
  - ROC curve
  - Precision/recall versus threshold line chart

EXAMPLE
Screening model for a rare outcome (about 8% prevalence), comparing two
classifiers.

Run:  python precision_recall_curve.py
      python precision_recall_curve.py --real-data   (real dataset: sklearn.datasets.load_breast_cancer() — Wisconsin diagnostic breast cancer, 569 tumours (malignant = positive), bundled with scikit-learn)
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

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve, average_precision_score

# --- Example data ------------------------------------------------------------
X, y = make_classification(n_samples=6000, n_features=20, n_informative=6, weights=[0.92],
                           flip_y=0.02, random_state=1)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=1, stratify=y)
models = {"Logistic regression": LogisticRegression(max_iter=1000),
          "Random forest": RandomForestClassifier(n_estimators=300, random_state=1)}
scores = {name: m.fit(X_tr, y_tr).predict_proba(X_te)[:, 1] for name, m in models.items()}
df = pd.DataFrame({"y_true": y_te, **scores})
print(f"prevalence = {df.y_true.mean():.3f}")
df.head()

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # sklearn.datasets.load_breast_cancer() — Wisconsin diagnostic breast cancer, 569 tumours (malignant = positive), bundled with scikit-learn
    from sklearn.datasets import load_breast_cancer
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    bc = load_breast_cancer()
    X, y = bc.data, 1 - bc.target                       # 1 = malignant
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=1, stratify=y)

    models = {"Logistic regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
              "Random forest": RandomForestClassifier(n_estimators=300, random_state=1)}
    scores = {name: m.fit(X_tr, y_tr).predict_proba(X_te)[:, 1] for name, m in models.items()}
    df = pd.DataFrame({"y_true": y_te, **scores})
    print(f"prevalence = {df.y_true.mean():.3f}")
    df.head()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 6))
for i, name in enumerate(scores):
    p, r, _ = precision_recall_curve(df["y_true"], df[name])
    ap = average_precision_score(df["y_true"], df[name])
    ax.plot(r, p, color=PALETTE[i], label=f"{name} (AP = {ap:.3f})")
prev = df["y_true"].mean()
ax.axhline(prev, color=GRAY, linewidth=1, label=f"No skill (prevalence = {prev:.2f})")
ax.set_xlabel("Recall (sensitivity)"); ax.set_ylabel("Precision (PPV)")
ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
ax.set_title("Precision–recall curve, test set")
ax.legend(loc="lower left")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
