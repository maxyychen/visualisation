# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from itertools import product

# %% data
rng = np.random.default_rng(2020)
choices = {  # option -> its (simulated) effect on the Sharpe ratio
    "Lookback": {"3 m": -0.25, "6 m": 0.0, "9 m": 0.05, "12 m": 0.08},
    "Skip last month": {"No": 0.0, "Yes": 0.08},
    "Rebalance": {"Monthly": 0.0, "Quarterly": -0.05},
    "Universe": {"Large caps": -0.12, "All stocks": 0.0, "Ex-financials": 0.03},
    "Trading cost": {"0 bp": 0.0, "10 bp": -0.12, "25 bp": -0.30},
    "Winsorise": {"None": 0.0, "1%": 0.02},
}
years = 20
specs = pd.DataFrame(list(product(*[list(v) for v in choices.values()])), columns=list(choices))
specs["sharpe"] = 0.55 + sum(specs[c].map(v) for c, v in choices.items()) + rng.normal(0, 0.04, len(specs))
se = np.sqrt((1 + 0.5 * specs["sharpe"] ** 2) / years)  # standard error of an annual Sharpe ratio
specs["lo"], specs["hi"] = specs["sharpe"] - 1.96 * se, specs["sharpe"] + 1.96 * se
specs = specs.sort_values("sharpe").reset_index(drop=True)
specs.describe().round(2)

# %% plot
sig_pos, sig_neg = specs["lo"] > 0, specs["hi"] < 0
col = np.where(sig_pos, PALETTE[0], np.where(sig_neg, PALETTE[1], "#a8a7a1"))
x = np.arange(len(specs))
rows = [(c, o) for c, opts in choices.items() for o in opts]

fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 8.2), sharex=True,
                             gridspec_kw={"height_ratios": [1, 1.25], "hspace": 0.06})
a1.vlines(x, specs["lo"], specs["hi"], color=col, alpha=0.25, linewidth=1)
a1.scatter(x, specs["sharpe"], s=9, color=col, zorder=3)
a1.axhline(0, color="#52514e", linewidth=1)
med = specs["sharpe"].median()
a1.axhline(med, color="#0b0b0b", linewidth=0.8)
a1.text(len(specs) + 2, med, f"median {med:.2f}", va="center", fontsize=8.5)
a1.set_ylabel("Annualised Sharpe ratio\n(dot = estimate, line = 95% CI)")
a1.set_title(f"{len(specs)} specifications · Sharpe > 0 in {(specs['sharpe'] > 0).mean():.0%} · "
             f"significantly > 0 in {sig_pos.mean():.0%} (blue)", fontsize=11)
a1.grid(axis="x", visible=False)

for r, (c, o) in enumerate(rows):
    on = specs[c] == o
    a2.scatter(x[on], np.full(on.sum(), r), s=6, marker="s", color=col[on], linewidths=0)
bounds = np.cumsum([len(v) for v in choices.values()])[:-1] - 0.5
for b in bounds:
    a2.axhline(b, color="#c9c8c3", linewidth=0.8)
a2.set_yticks(range(len(rows)), [o for _, o in rows], fontsize=8.5)
start = 0
for c, opts in choices.items():  # choice names in the left margin
    a2.text(-0.11, start + (len(opts) - 1) / 2, c, transform=a2.get_yaxis_transform(), ha="right",
            va="center", fontsize=9, fontweight="bold")
    start += len(opts)
a2.set_ylim(len(rows) - 0.5, -0.5)
a2.set_xlim(-3, len(specs) + 30)
a2.set_xlabel("Specifications, sorted by estimated Sharpe ratio")
a2.grid(False)

fig.suptitle("Momentum strategy: is the result robust to analyst choices? (simulated)", x=0.01, ha="left",
             fontweight="bold", fontsize=13)
fig.subplots_adjust(left=0.2, right=0.97, top=0.91, bottom=0.07)
