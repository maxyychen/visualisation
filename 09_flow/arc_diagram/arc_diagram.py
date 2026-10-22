"""
Arc Diagram  -  family: Flow

DESIGN PURPOSE
Nodes are placed along a single line and connections are drawn as arcs above
it. The one-dimensional layout makes node order meaningful (time, sequence, or
group). Arc height shows how far apart connected nodes are.

WHEN TO USE
  - Show connections where node order matters (characters by first appearance,
    sequential steps)
  - Show co-occurrence or links within a sequence (repeated motifs,
    references)
  - Show a cleaner network layout for small graphs

AVOID WHEN
  - The network is large or dense (arcs overlap heavily)
  - Structure such as clusters matters more than order (use a force-directed
    network)

ALTERNATIVES
  - Network graph
  - Adjacency matrix
  - Chord diagram

EXAMPLE
Board interlocks among 12 listed companies, where two firms are linked when
they share directors (synthetic).

Run:  python arc_diagram.py
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

from matplotlib.patches import Arc

# --- Example data ------------------------------------------------------------
chapters = [f"Co {c}" for c in "ABCDEFGHIJKL"]
refs = pd.DataFrame([(1, 3, 2), (1, 5, 1), (2, 3, 3), (2, 8, 1), (3, 4, 4), (3, 9, 2),
                     (4, 6, 2), (5, 6, 3), (5, 11, 1), (6, 7, 2), (7, 10, 3), (8, 9, 2),
                     (9, 12, 1), (10, 11, 2), (1, 12, 1), (4, 10, 1)],
                    columns=["from", "to", "refs"])  # refs = shared directors
refs.head()

# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.8))
for f, t, w in refs.itertuples(index=False):
    center, width = (f + t) / 2, abs(t - f)
    ax.add_patch(Arc((center, 0), width, width, theta1=0, theta2=180,
                     color=PALETTE[0], linewidth=0.8 + 1.0 * w, alpha=0.6))
strength = refs.groupby("from")["refs"].sum().add(refs.groupby("to")["refs"].sum(), fill_value=0)
xs = np.arange(1, 13)
ax.scatter(xs, np.zeros(12), s=[40 + 25 * strength.get(i, 0) for i in xs], color=PALETTE[1],
           zorder=3, edgecolor="#fcfcfb", linewidth=1.5)
for x, c in zip(xs, chapters):
    ax.text(x, -0.35, c, ha="center", va="top", fontsize=9)
ax.set_xlim(0.3, 12.7)
ax.set_ylim(-1, 6.2)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Board interlocks among 12 listed companies (arc width = shared directors)")
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
