# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.ticker import PercentFormatter

# %% data
rng = np.random.default_rng(21)
dates = pd.bdate_range("2015-01-01", "2024-12-31")
n = len(dates)
mkt = 0.00045 + rng.standard_t(4, n) * 0.0095 / np.sqrt(2)
mkt[(dates >= "2020-02-20") & (dates <= "2020-03-23")] -= 0.012
mkt[(dates >= "2022-01-01") & (dates <= "2022-10-15")] -= 0.0011
fund = 0.00024 + 0.9 * mkt + rng.normal(0, 0.004, n)
rets = pd.DataFrame({"Fund": fund, "Benchmark": mkt}, index=dates)  # simple daily returns
freq, window, rf = 252, 252, 0.02   # obs/year, rolling window, annual risk-free rate
rets.head()

# %% real-data
import plotly.express as px
stocks = px.data.stocks().set_index("date")
stocks.index = pd.to_datetime(stocks.index)
weekly = stocks.pct_change().dropna()
rets = pd.DataFrame({"AMZN": weekly["AMZN"], "Tech basket": weekly.mean(axis=1)})
freq, window, rf = 52, 26, 0.02
rets.head()

# %% plot
roll_ret = (1 + rets).rolling(window).apply(np.prod, raw=True) ** (freq / window) - 1
roll_vol = rets.rolling(window).std() * np.sqrt(freq)
roll_sharpe = (rets.rolling(window).mean() * freq - rf) / roll_vol
fund_name, bench_name = rets.columns[:2]

fig, axes = plt.subplots(3, 1, figsize=(9, 7.5), sharex=True)
panels = [(roll_ret, "Return (annualised)", True), (roll_vol, "Volatility (annualised)", True),
          (roll_sharpe, "Sharpe ratio", False)]
for ax, (data, label, pct) in zip(axes, panels):
    ax.plot(data.index, data[bench_name], color=GRAY, linewidth=1.5, label=bench_name)
    ax.plot(data.index, data[fund_name], color=PALETTE[0], linewidth=1.8, label=fund_name)
    if label != "Volatility (annualised)":
        ax.axhline(0, color="#52514e", linewidth=0.9)
    if pct:
        ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_ylabel(label)
axes[0].set_title(f"Rolling {window}-period metrics: {fund_name} vs. {bench_name}")
axes[0].legend(loc="upper left", ncol=2)
fig.tight_layout()
