# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.ticker import PercentFormatter

# %% data
assets = ["US equities", "Intl equities", "Gov. bonds", "Corp. bonds", "Gold", "Cash"]
weights = pd.Series([0.35, 0.15, 0.25, 0.15, 0.05, 0.05], index=assets)
vol = np.array([0.16, 0.18, 0.06, 0.07, 0.15, 0.005])          # annualised volatility
corr = np.array([[1.0, 0.85, -0.2, 0.3, 0.05, 0.0],
                 [0.85, 1.0, -0.15, 0.3, 0.1, 0.0],
                 [-0.2, -0.15, 1.0, 0.6, 0.25, 0.1],
                 [0.3, 0.3, 0.6, 1.0, 0.15, 0.1],
                 [0.05, 0.1, 0.25, 0.15, 1.0, 0.0],
                 [0.0, 0.0, 0.1, 0.1, 0.0, 1.0]])
cov = pd.DataFrame(np.outer(vol, vol) * corr, index=assets, columns=assets)
weights

# %% real-data
import plotly.express as px
stocks = px.data.stocks().set_index("date")
cov = stocks.pct_change().dropna().cov() * 52           # annualised from weekly returns
weights = pd.Series(1 / len(cov), index=cov.index)
weights

# %% plot
w = weights.values
port_var = w @ cov.values @ w
rc = pd.Series(w * (cov.values @ w) / port_var, index=weights.index)  # sums to 1
order = rc.sort_values().index
y = np.arange(len(order))
fig, ax = plt.subplots(figsize=(8.5, 0.55 * len(order) + 1.6))
ax.barh(y + 0.19, weights[order], height=0.36, color=GRAY, label="Share of capital")
ax.barh(y - 0.19, rc[order], height=0.36, color=PALETTE[0], label="Share of risk")
for yi, a in zip(y, order):
    ax.text(weights[a] + 0.006, yi + 0.19, f"{weights[a]:.0%}", va="center", fontsize=8.5, color="#52514e")
    ax.text(max(rc[a], 0) + 0.006, yi - 0.19, f"{rc[a]:.0%}", va="center", fontsize=8.5, color="#0b0b0b")
ax.axvline(0, color="#52514e", linewidth=1)
ax.set_yticks(y, order)
ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
ax.set_xlim(min(0, rc.min() * 1.2), max(rc.max(), weights.max()) * 1.15)
ax.grid(axis="y", visible=False)
ax.set_title(f"Capital vs. risk (portfolio volatility {np.sqrt(port_var):.1%} a year)")
ax.legend(loc="lower right")
fig.tight_layout()
