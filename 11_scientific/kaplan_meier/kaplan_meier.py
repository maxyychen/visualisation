"""
Kaplan–Meier Survival Curve  -  family: Scientific

DESIGN PURPOSE
A step function estimating the probability of remaining event-free over time
while correctly handling censored subjects, meaning those whose follow-up
ended before an event. It is the standard figure for time-to-event outcomes in
clinical trials and cohort studies.

WHEN TO USE
  - Compare overall survival, progression-free survival or time-to-relapse
    between treatment arms or risk groups
  - Show any time-to-event outcome with censoring (churn, machine failure,
    time to readmission)
  - Report median survival and survival at landmark times (1-year, 5-year)

AVOID WHEN
  - Survival curves cross substantially (the log-rank test is weak; report
    RMST or landmark analyses as well)
  - There are competing risks (use cumulative incidence functions)
  - There are many groups (more than 3–4 curves become unreadable; facet
    instead)

ALTERNATIVES
  - Cumulative incidence plot
  - Swimmer plot (patient-level detail)
  - Forest plot of hazard ratios

EXAMPLE
A simulated two-arm oncology trial (120 patients per arm): median overall
survival is about 12 months on control and 18 months on the new treatment,
with administrative censoring at up to 48 months.

Run:  python kaplan_meier.py
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

from scipy.stats import chi2

# --- Example data ------------------------------------------------------------
rng = np.random.default_rng(42)
def simulate(n, median):
    event_time = rng.exponential(median / np.log(2), n)
    censor_time = np.minimum(rng.uniform(12, 48, n), rng.exponential(80, n))
    t = np.minimum(event_time, censor_time).round(1)
    return t, (event_time <= censor_time).astype(int)
arms = {"Control": simulate(120, 12), "New treatment": simulate(120, 18)}
df = pd.concat([pd.DataFrame({"arm": a, "months": t, "event": e}) for a, (t, e) in arms.items()])

def kaplan_meier(t, e):
    """Kaplan-Meier estimate with Greenwood 95% CI. Returns step times and S(t)."""
    times = np.unique(t[e == 1])
    n = np.array([(t >= u).sum() for u in times])
    d = np.array([((t == u) & (e == 1)).sum() for u in times])
    s = np.cumprod(1 - d / n)
    denom = n * (n - d)
    gw = np.cumsum(np.divide(d, denom, out=np.zeros(len(d)), where=denom > 0))
    se = s * np.sqrt(gw)
    lo, hi = np.clip(s - 1.96 * se, 0, 1), np.clip(s + 1.96 * se, 0, 1)
    end = max(t.max(), times.max())  # carry the last estimate out to the last follow-up
    return (np.r_[0, times, end], np.r_[1, s, s[-1]], np.r_[1, lo, lo[-1]], np.r_[1, hi, hi[-1]])

def logrank_p(t1, e1, t2, e2):
    O = E = V = 0.0
    for u in np.unique(np.r_[t1[e1 == 1], t2[e2 == 1]]):
        n1, n2 = (t1 >= u).sum(), (t2 >= u).sum()
        d1, d = ((t1 == u) & (e1 == 1)).sum(), ((t1 == u) & (e1 == 1)).sum() + ((t2 == u) & (e2 == 1)).sum()
        n = n1 + n2
        O += d1; E += d * n1 / n
        if n > 1:
            V += d * (n1 / n) * (n2 / n) * (n - d) / (n - 1)
    return chi2.sf((O - E) ** 2 / V, 1)

p_value = logrank_p(*arms["Control"], *arms["New treatment"])
df.groupby("arm").agg(patients=("event", "size"), events=("event", "sum"))

# --- Plot --------------------------------------------------------------------
fig, (ax, axr) = plt.subplots(2, 1, figsize=(9, 6.6), height_ratios=[4, 1.1], sharex=True)
ticks = np.arange(0, 49, 6)
for i, (arm, (t, e)) in enumerate(arms.items()):
    x, s, lo, hi = kaplan_meier(t, e)
    med = x[np.argmax(s <= 0.5)] if (s <= 0.5).any() else np.nan
    ax.step(x, s, where="post", color=PALETTE[i], label=f"{arm} (median {med:.1f} mo)")
    ax.fill_between(x, lo, hi, step="post", color=PALETTE[i], alpha=0.15, linewidth=0)
    ct = t[e == 0]
    ax.plot(ct, s[np.searchsorted(x, ct, side="right") - 1], "|", color=PALETTE[i], markersize=7)
    for tk in ticks:
        axr.text(tk, 1 - i, str((t >= tk).sum()), ha="center", va="center", color=PALETTE[i], fontsize=9)
ax.axhline(0.5, color="#c9c8c3", linewidth=0.8)
ax.set_ylim(0, 1.02); ax.set_ylabel("Overall survival probability")
ax.set_title("Overall survival by treatment arm")
ax.text(0.98, 0.95, "Log-rank p < 0.001" if p_value < 0.001 else f"Log-rank p = {p_value:.3f}", transform=ax.transAxes, ha="right", color="#52514e")
ax.legend(loc="lower left")
axr.set_ylim(-0.6, 1.6); axr.set_yticks([1, 0], list(arms)); axr.grid(False)
axr.set_xticks(ticks); axr.set_xlim(-1, 49); axr.set_xlabel("Months since randomisation")
axr.set_title("Number at risk", fontsize=10, fontweight="normal")
for side in ("left", "bottom"):
    axr.spines[side].set_visible(False)
axr.tick_params(length=0)
fig.tight_layout()

# --- Save / show -------------------------------------------------------------
out = Path(__file__).with_name(Path(__file__).stem + ".png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
if "--no-show" not in sys.argv:
    plt.show()
