"""
Lineup Protocol (visual inference)  -  family: Scientific

DESIGN PURPOSE
Hides the real chart among 19 "null" charts generated from data where the
pattern cannot exist, for example by shuffling the order of returns. If an
honest viewer can pick out the real chart, the pattern is unlikely to be
chance (p ≈ 1/20 = 0.05 for one viewer). The chart becomes a statistical test,
with human perception as the test statistic.

WHEN TO USE
  - Check whether a pattern you see (a trend, momentum, clustering, a spatial
    hot spot) is real or a trick of the eye
  - Test a pattern for which no convenient formal test exists
  - Teach analysts how easily randomness produces convincing-looking patterns

AVOID WHEN
  - A standard formal test answers the question directly and the audience
    trusts it
  - The viewer has already seen the real chart (they will recognise it, which
    invalidates the test)
  - Final presentation of a result (show the finding itself; keep the lineup
    in the appendix or the analysis)

ALTERNATIVES
  - Rorschach plots (all nulls, to calibrate your eye)
  - A permutation test reported as a number

REFERENCE
  - Buja, A., Cook, D., Hofmann, H., Lawrence, M., Lee, E.-K., Swayne, D. F. &
    Wickham, H. (2009). Statistical inference for exploratory data analysis
    and model diagnostics. Philosophical Transactions of the Royal Society A
    367, 4361–4383. https://doi.org/10.1098/rsta.2009.0120
  - Wickham, H., Cook, D., Hofmann, H. & Buja, A. (2010). Graphical inference
    for infovis. IEEE Transactions on Visualization and Computer Graphics
    16(6), 973–979. https://vita.had.co.nz/papers/inference-infovis.html

EXAMPLE
A simulated weekly price series with momentum (positive autocorrelation in
returns) placed at a random position among 19 series built by shuffling its
own weekly returns. The real-data variant does the same with Apple's weekly
returns, 2018–2019.

Run:  python lineup_protocol.py
      python lineup_protocol.py --real-data   (real dataset: plotly.express.data.stocks (AAPL weekly returns, 2018–2019))
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
rng = np.random.default_rng(2010)
n = 156  # three years of weekly returns
eps = rng.normal(0, 0.02, n)
real = np.empty(n)
real[0] = eps[0]
for t in range(1, n):  # momentum: this week's return carries over into the next
    real[t] = 0.6 * real[t - 1] + eps[t]
real += 0.001
answer = 15  # position of the real series (keep it secret from your viewers)


def lineup(real_returns, answer, n_panels=20, seed=0):
    """Price paths: the real one at `answer`, the rest from shuffled copies of its returns."""
    g = np.random.default_rng(seed)
    paths = [g.permutation(real_returns) for _ in range(n_panels)]
    paths[answer - 1] = real_returns
    return [100 * np.cumprod(1 + r) for r in paths]


panels = lineup(real, answer)
title = "Which price path is real? The other 19 are shuffled copies of its weekly returns (simulated)"
f"lag-1 autocorrelation of the real returns: {np.corrcoef(real[:-1], real[1:])[0, 1]:.2f}"

REAL_DATA = "--real-data" in sys.argv
if REAL_DATA:  # plotly.express.data.stocks (AAPL weekly returns, 2018–2019)
    import plotly.express as px

    real = px.data.stocks()["AAPL"].pct_change().dropna().to_numpy()
    answer = 7
    panels = lineup(real, answer)
    title = "Which is Apple's real weekly price path (2018–2019)? The other 19 are shuffled copies of its returns"
    f"lag-1 autocorrelation of AAPL weekly returns: {np.corrcoef(real[:-1], real[1:])[0, 1]:.2f}"

# --- Plot --------------------------------------------------------------------
fig, axes = plt.subplots(4, 5, figsize=(11, 7.6))
for k, (ax, path) in enumerate(zip(axes.flat, panels), start=1):
    ax.plot(path, color=PALETTE[0], linewidth=1.3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.set_facecolor("#f4f3f0")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.text(0.04, 0.86, str(k), transform=ax.transAxes, fontsize=10, color="#52514e", fontweight="bold")
fig.suptitle(title, x=0.01, ha="left", fontweight="bold", fontsize=12.5)
fig.text(0.99, 0.008, f"Answer: panel {answer} is the real series; the others are permutations of its returns.",
         ha="right", fontsize=7.5, color="#8f8e88")
fig.tight_layout(rect=(0, 0.025, 1, 0.96))

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ("_real" if REAL_DATA else "") + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
