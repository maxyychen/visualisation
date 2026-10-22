# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.ticker import PercentFormatter

# %% data
rng = np.random.default_rng(12)
vol = rng.uniform(0.08, 0.24, 30)
ret = 0.02 + 0.35 * vol + rng.normal(0, 0.025, 30)
stats = pd.DataFrame({"ann_vol": vol, "ann_return": ret}, index=[f"Peer {i:02d}" for i in range(1, 31)])
stats.loc["Our fund"] = [0.155, 0.112]
stats.loc["Benchmark"] = [0.15, 0.085]
highlight, benchmark, rf = "Our fund", "Benchmark", 0.02
stats.tail()

# %% real-data
import plotly.express as px
prices = px.data.stocks().set_index("date")
weekly = prices.pct_change().dropna()
weekly["Equal-weight"] = weekly.mean(axis=1)
stats = pd.DataFrame({"ann_vol": weekly.std() * np.sqrt(52),
                      "ann_return": (1 + weekly).prod() ** (52 / len(weekly)) - 1})
highlight, benchmark, rf = "AAPL", "Equal-weight", 0.02
stats

# %% plot
fig, ax = plt.subplots(figsize=(8.5, 6))
others = stats.drop([highlight, benchmark])
xmax = stats["ann_vol"].max() * 1.15
for sharpe in [0.25, 0.5, 0.75, 1.0, 1.5]:
    ax.plot([0, xmax], [rf, rf + sharpe * xmax], color="#e6e5e1", linewidth=1, zorder=1)
    y_end = rf + sharpe * xmax
    if y_end < stats["ann_return"].max() * 1.15:
        ax.text(xmax, y_end, f" SR {sharpe}", fontsize=8, color="#7a7974", va="center")
ax.scatter(others["ann_vol"], others["ann_return"], s=40, color=GRAY, edgecolor="#fcfcfb", linewidth=1, zorder=2)
if len(others) <= 8:  # few peers: name them
    for name, (x, y) in others.iterrows():
        ax.annotate(name, (x, y), xytext=(7, 0), textcoords="offset points", va="center", fontsize=8.5,
                    color="#52514e")
for name, color in [(benchmark, PALETTE[1]), (highlight, PALETTE[0])]:
    x, y = stats.loc[name]
    ax.scatter(x, y, s=110, color=color, edgecolor="#fcfcfb", linewidth=2, zorder=3)
    left = name == benchmark
    ax.annotate(f"{name}\nSharpe {(y - rf) / x:.2f}", (x, y), xytext=(-10 if left else 10, 0),
                textcoords="offset points", ha="right" if left else "left", va="center", fontsize=9,
                weight="bold", color="#0b0b0b")
ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
ax.set_xlim(0, xmax)
ax.set_ylim(min(0, stats["ann_return"].min() * 1.1), stats["ann_return"].max() * 1.15)
ax.set_xlabel("Volatility (annualised)")
ax.set_ylabel("Return (annualised)")
ax.set_title(f"{highlight} vs. peers: return per unit of risk")
fig.tight_layout()
