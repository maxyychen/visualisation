# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from vizlib.finance import tear_sheet, summary_stats

# %% data
rng = np.random.default_rng(41)
dates = pd.bdate_range("2018-01-01", "2024-12-31")
n = len(dates)
# Market: calm drift, a sharp crash (~day 560) and a slow bear market (~day 1200).
market = rng.standard_t(4, n) * 0.007 + 0.0005
market[555:575] -= 0.010
market[1180:1380] -= 0.0008
# Fund: beta 0.85 to the market plus a small, noisy alpha.
fund = 0.85 * market + rng.normal(0.00012, 0.004, n)
returns = pd.Series(fund, index=dates, name="Fund")
benchmark = pd.Series(market, index=dates, name="Index")
title = "Global Equity Fund: performance report (simulated)"
summary_stats(returns, benchmark).style.format("{:.3f}")

# %% plot
fig = tear_sheet(returns, benchmark, title=title, rf=0.02)

# %% real-data
import plotly.express as px

stocks = px.data.stocks().assign(date=lambda d: pd.to_datetime(d["date"])).set_index("date")
returns = stocks["AAPL"].pct_change().dropna().rename("AAPL")
benchmark = stocks.pct_change().dropna().mean(axis=1).rename("Equal-weight tech")
title = "AAPL vs. equal-weight big tech, weekly 2018–2019"
summary_stats(returns, benchmark).style.format("{:.3f}")
