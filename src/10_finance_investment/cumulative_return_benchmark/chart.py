# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.ticker import FuncFormatter, LogLocator

# %% data
# Simulated daily simple returns: fat-tailed market (Student-t, 4 df) plus a fund with beta 0.9.
rng = np.random.default_rng(21)
dates = pd.bdate_range("2015-01-01", "2024-12-31")
n = len(dates)
mkt = 0.00045 + rng.standard_t(4, n) * 0.0095 / np.sqrt(2)
crash = (dates >= "2020-02-20") & (dates <= "2020-03-23")
mkt[crash] -= 0.012
mkt[(dates >= "2022-01-01") & (dates <= "2022-10-15")] -= 0.0011
fund = 0.00024 + 0.9 * mkt + rng.normal(0, 0.004, n)
fund[0] = mkt[0] = 0.0  # the first date is the start: both series begin at exactly 10,000
prices = 10_000 * (1 + pd.DataFrame({"Fund": fund, "Benchmark": mkt}, index=dates)).cumprod()
freq = 252  # observations per year, used for CAGR
prices.tail()

# %% real-data
import plotly.express as px
stocks = px.data.stocks().set_index("date")
stocks.index = pd.to_datetime(stocks.index)
basket = stocks.pct_change().mean(axis=1).fillna(0).add(1).cumprod()  # equal-weight, rebalanced weekly
prices = 10_000 * pd.DataFrame({"AAPL": stocks["AAPL"], "Tech basket": basket})
freq = 52
prices.tail()

# %% plot
fund_name, bench_name = prices.columns[:2]
years = (len(prices) - 1) / freq  # n prices span n - 1 return periods
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(prices.index, prices[bench_name], color=GRAY, linewidth=1.6, label=bench_name)
ax.plot(prices.index, prices[fund_name], color=PALETTE[0], linewidth=2, label=fund_name)
ax.set_yscale("log")
ax.yaxis.set_major_locator(LogLocator(base=10, subs=[1, 1.5, 2, 3, 5, 7]))
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.yaxis.set_minor_formatter(FuncFormatter(lambda v, _: ""))
for name, color in [(fund_name, PALETTE[0]), (bench_name, "#52514e")]:
    end = prices[name].iloc[-1]
    cagr = (end / prices[name].iloc[0]) ** (1 / years) - 1
    ax.annotate(f"{name}\n{end:,.0f}  ({cagr:+.1%}/yr)", (prices.index[-1], end),
                xytext=(8, 0), textcoords="offset points", va="center", fontsize=9, color=color)
ax.set_ylabel("Value of 10,000 invested (log scale)")
ax.set_title(f"Growth of 10,000: {fund_name} vs. {bench_name}")
ax.legend(loc="upper left")
ax.margins(x=0.01)
fig.tight_layout()
