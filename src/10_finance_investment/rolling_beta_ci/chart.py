# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm

# %% data
rng = np.random.default_rng(17)
dates = pd.bdate_range("2016-01-01", "2024-12-31")
n = len(dates)
true_beta = pd.Series(np.interp(np.arange(n), [0, 700, 1400, 1800, n - 1], [0.8, 0.8, 1.4, 1.0, 1.0]), index=dates)
market = rng.normal(0.0004, 0.010, n)
stock = 0.0001 + true_beta.values * market + rng.normal(0, 0.012, n)
rets = pd.DataFrame({"stock": stock, "market": market}, index=dates)
window = 252
label = "Stock"
title = "Rolling 1-year beta: market exposure is not constant (simulated)"
rets.head()

# %% plot
res = RollingOLS(rets["stock"], sm.add_constant(rets["market"]), window=window).fit()
beta = res.params["market"]
se = res.bse["market"]
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.fill_between(beta.index, beta - 1.96 * se, beta + 1.96 * se, color=PALETTE[0], alpha=0.2,
                linewidth=0, label="95% confidence band")
ax.plot(beta.index, beta, color=PALETTE[0], label=f"{label}: estimated beta")
if true_beta is not None:
    ax.plot(true_beta.index, true_beta, color="#8f8e88", linewidth=1, label="True beta (simulation)")
ax.axhline(1, color="#52514e", linewidth=0.9)
ax.text(beta.dropna().index[0], 1.01, "β = 1 (moves with the market)", fontsize=8, color="#52514e", va="bottom")
ax.set_ylabel(f"Beta ({window}-period window)")
ax.set_title(title)
ax.legend(loc="upper left", fontsize=9)
fig.tight_layout()

# %% real-data
import plotly.express as px

stocks = px.data.stocks().assign(date=lambda d: pd.to_datetime(d["date"])).set_index("date")
weekly = stocks.pct_change().dropna()
rets = pd.DataFrame({"stock": weekly["AAPL"], "market": weekly.mean(axis=1)})
window = 52
label = "AAPL"
true_beta = None
title = "AAPL rolling 52-week beta vs. equal-weight big tech"
rets.head()
