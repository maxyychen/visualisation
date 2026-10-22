# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.ticker import PercentFormatter
import matplotlib.dates as mdates

# %% data
rng = np.random.default_rng(21)
dates = pd.bdate_range("2015-01-01", "2024-12-31")
n = len(dates)
eq = 0.00045 + rng.standard_t(4, n) * 0.0095 / np.sqrt(2)
eq[(dates >= "2020-02-20") & (dates <= "2020-03-23")] -= 0.012
bonds = 0.00012 + rng.normal(0, 0.0035, n)
cash = np.full(n, 0.00006)
asset_rets = pd.DataFrame({"Equities": eq, "Bonds": bonds, "Cash": cash}, index=dates)
target = pd.Series({"Equities": 0.6, "Bonds": 0.3, "Cash": 0.1})
asset_rets.head()

# %% plot
def simulate(rebalance):
    holdings = target.values.copy()
    out = np.empty((len(asset_rets), len(target)))
    years = asset_rets.index.year
    for i, r in enumerate(asset_rets.values):
        if rebalance and i > 0 and years[i] != years[i - 1]:
            holdings = holdings.sum() * target.values
        holdings = holdings * (1 + r)
        out[i] = holdings / holdings.sum()
    return pd.DataFrame(out, index=asset_rets.index, columns=target.index)

panels = [("Rebalanced every January", simulate(True)), ("Never rebalanced", simulate(False))]
colors = [PALETTE[0], PALETTE[1], PALETTE[3]]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
for ax, (title, w) in zip(axes, panels):
    ax.stackplot(w.index, w.T.values, colors=colors, labels=w.columns, edgecolor="#fcfcfb", linewidth=0.6)
    for cum in target.cumsum().values[:-1]:
        ax.axhline(cum, color="#0b0b0b", linewidth=0.8, alpha=0.6)
    ax.text(w.index[-60], w["Equities"].iloc[-1] / 2, f"Equities now\n{w['Equities'].iloc[-1]:.0%}",
            fontsize=9.5, ha="right", va="center", color="white", weight="bold")
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_title(title)
    ax.set_ylim(0, 1)
    ax.margins(x=0)
    ax.grid(False)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
axes[0].set_ylabel("Portfolio weight")
axes[1].legend(loc="upper center", bbox_to_anchor=(-0.05, -0.08), ncol=3)
fig.suptitle("A 60/40/10 portfolio drifts unless it is rebalanced (thin lines = target)", x=0.02,
             ha="left", fontsize=13, weight="bold")
fig.tight_layout()
