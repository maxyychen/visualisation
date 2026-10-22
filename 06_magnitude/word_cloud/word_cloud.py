"""
Word Cloud  -  family: Magnitude

DESIGN PURPOSE
Shows words from a text sized by their frequency. It gives an at-a-glance,
impressionistic summary of the dominant terms in open-ended text.

WHEN TO USE
  - Give a quick first look at the themes of free-text responses, reviews or
    speeches
  - Engaging illustrations where precision is not required

AVOID WHEN
  - Any analytical comparison (word size is confounded by word length; use a
    bar chart of frequencies)
  - Small corpora, or text where key phrases span several words

ALTERNATIVES
  - Horizontal bar chart of top terms
  - Treemap of topics

EXAMPLE
Word frequencies from app-store reviews of a mobile banking app (synthetic).

Run:  python word_cloud.py
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
from collections import Counter
rng = np.random.default_rng(2)
vocab = {"easy": 40, "transfer": 34, "login": 30, "fast": 28, "fees": 26, "support": 24,
         "update": 22, "crash": 18, "secure": 16, "card": 15, "budget": 14, "savings": 12,
         "notifications": 11, "statement": 10, "investing": 9, "biometric": 8, "slow": 7,
         "exchange": 6, "interest": 6, "cashback": 5, "outage": 4, "verification": 4, "loan": 3}
freqs = {w: int(f * rng.uniform(0.8, 1.2)) for w, f in vocab.items()}
pd.Series(freqs).sort_values(ascending=False).head(10)

# --- Plot --------------------------------------------------------------------
from wordcloud import WordCloud
blues = ["#104281", "#1c5cab", "#2a78d6", "#5598e7"]
wc = WordCloud(width=1000, height=500, background_color="#fcfcfb", prefer_horizontal=0.9,
               color_func=lambda *a, **k: blues[np.random.default_rng(len(a[0])).integers(4)],
               random_state=1).generate_from_frequencies(freqs)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), gridspec_kw={"width_ratios": [2, 1]})
ax1.imshow(wc, interpolation="bilinear")
ax1.axis("off")
ax1.set_title("Banking app reviews: most frequent words")
top = pd.Series(freqs).sort_values().tail(10)
ax2.barh(top.index, top.values, color=PALETTE[0], height=0.7)
ax2.set_title("Top 10 terms (precise)")
ax2.set_xlabel("Mentions")
ax2.grid(axis="y", visible=False)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
