# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from statsmodels.tsa.stattools import acf, pacf

# %% data
rng = np.random.default_rng(9)
n = 365
dates = pd.date_range("2024-01-01", periods=n, freq="D")
weekly = np.array([0.4, 0.5, 0.5, 0.45, 0.3, -1.1, -1.05])      # Mon..Sun effect
x = np.zeros(n)
for t in range(1, n):
    x[t] = 0.55 * x[t - 1] + rng.normal(0, 0.6)
series = pd.Series(x + weekly[dates.dayofweek], index=dates, name="sessions (std. units)")
nlags = 28
series.head(8).round(2)

# %% plot
fig = plt.figure(figsize=(11, 6.4))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.15], hspace=0.45, wspace=0.15)
ax0 = fig.add_subplot(gs[0, :])
ax0.plot(series.index, series, color=PALETTE[0], linewidth=1)
ax0.axhline(0, color="#52514e", linewidth=0.8)
ax0.set_title("The series: daily website sessions, detrended (simulated)", fontsize=11)

for k, (name, fn) in enumerate([("ACF: autocorrelation", acf), ("PACF: partial autocorrelation", pacf)]):
    ax = fig.add_subplot(gs[1, k], sharey=None)
    vals, ci = (fn(series, nlags=nlags, alpha=0.05) if fn is pacf
                else fn(series, nlags=nlags, alpha=0.05, fft=True))
    lags = np.arange(len(vals))
    band = ci[:, 1] - vals
    ax.fill_between(lags[1:], -band[1:], band[1:], color="#e4eefb", step="mid", linewidth=0,
                    label="95% band (no correlation)")
    ax.vlines(lags[1:], 0, vals[1:], color=PALETTE[0], linewidth=2)
    ax.scatter(lags[1:], vals[1:], color=PALETTE[0], s=14, zorder=3)
    ax.axhline(0, color="#52514e", linewidth=0.8)
    for s in (7, 14, 21, 28):
        ax.axvline(s, color="#e6e5e1", linewidth=3, zorder=0)
    ax.set_xticks([1, 7, 14, 21, 28])
    ax.set_xlabel("Lag (days)")
    ax.set_ylim(-0.6, 1)
    ax.set_title(name, fontsize=11)
    if k == 0:
        ax.legend(loc="upper right", fontsize=8)
fig.suptitle("Autocorrelation reveals memory and a weekly cycle", x=0.06, ha="left",
             fontsize=14, fontweight="bold")
