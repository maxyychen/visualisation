# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.ticker import PercentFormatter, LogLocator, FuncFormatter

# %% data
rng = np.random.default_rng(21)
dates = pd.bdate_range("2015-01-01", "2024-12-31")
n = len(dates)
r = 0.00045 + rng.standard_t(4, n) * 0.0095 / np.sqrt(2)
r[(dates >= "2020-02-20") & (dates <= "2020-03-23")] -= 0.012
r[(dates >= "2022-01-01") & (dates <= "2022-10-15")] -= 0.0011
price = pd.Series(100 * np.cumprod(1 + r), index=dates, name="Fund")
price.tail()

# %% real-data
import plotly.express as px
stocks = px.data.stocks().set_index("date")
price = pd.Series(100 * stocks["NFLX"].values, index=pd.to_datetime(stocks.index), name="NFLX")
price.tail()

# %% plot
drawdown = price / price.cummax() - 1
trough = drawdown.idxmin()
peak = price.loc[:trough].idxmax()
recovered = price.loc[trough:][price.loc[trough:] >= price.loc[peak]]
recovery = recovered.index[0] if len(recovered) else None

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True,
                               gridspec_kw={"height_ratios": [1.3, 1]})
ax1.plot(price.index, price, color=PALETTE[0])
ax1.set_yscale("log")
ax1.yaxis.set_major_locator(LogLocator(base=10, subs=[1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 7]))
ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax1.yaxis.set_minor_formatter(FuncFormatter(lambda v, _: ""))
ax1.set_ylabel("Price (log scale)")
ax1.set_title(f"{price.name}: price and drawdown from previous peak")
ax1.axvspan(peak, recovery or price.index[-1], color=PALETTE[1], alpha=0.08, linewidth=0)

ax2.fill_between(drawdown.index, drawdown, 0, color=PALETTE[1], alpha=0.85, linewidth=0)
ax2.axhline(0, color="#52514e", linewidth=1)
ax2.yaxis.set_major_formatter(PercentFormatter(1.0))
ax2.set_ylabel("Drawdown")
rec_text = f"recovered {recovery:%b %Y}" if recovery is not None else "not yet recovered"
ax2.annotate(f"Max drawdown {drawdown.min():.1%}\npeak {peak:%b %Y} → trough {trough:%b %Y}, {rec_text}",
             (trough, drawdown.min()), xytext=(14, 4), textcoords="offset points", fontsize=9,
             va="bottom", color="#0b0b0b")
ax2.set_ylim(drawdown.min() * 1.25, 0.02)
fig.tight_layout()
