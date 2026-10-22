# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
from scipy import stats
rng = np.random.default_rng(9)
hist_dates = pd.date_range("2021-01", periods=48, freq="MS")
hist = 200 + 2 * np.arange(48) + 15 * np.sin(np.arange(48) * 2 * np.pi / 12) + rng.normal(0, 6, 48)
fc_dates = pd.date_range(hist_dates[-1], periods=13, freq="MS")
h = np.arange(13)
center = hist[-1] + 2 * h + 15 * (np.sin((48 + h - 1) * 2 * np.pi / 12) - np.sin(47 * 2 * np.pi / 12))
sd = 4 + 3.0 * np.sqrt(h)
bands = {lvl: (center - stats.norm.ppf(0.5 + lvl / 2) * sd, center + stats.norm.ppf(0.5 + lvl / 2) * sd)
         for lvl in (0.5, 0.8, 0.95)}
forecast = pd.DataFrame({"date": fc_dates, "center": center, "sd": sd})
forecast.head()

# %% plot
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(hist_dates, hist, color="#0b0b0b", linewidth=1.5, label="Observed")
for lvl, alpha in [(0.95, 0.15), (0.8, 0.25), (0.5, 0.4)]:
    lo, hi = bands[lvl]
    ax.fill_between(fc_dates, lo, hi, color=PALETTE[0], alpha=alpha, linewidth=0,
                    label=f"{int(lvl * 100)}% interval")
ax.plot(fc_dates, center, color=PALETTE[0], linewidth=2, label="Forecast")
ax.axvline(hist_dates[-1], color="#52514e", linewidth=1)
ax.text(hist_dates[-1], ax.get_ylim()[1], "  forecast →", va="top", color="#52514e")
ax.set_ylabel("Units (k)")
ax.set_title("Monthly demand with 12-month forecast")
ax.legend(loc="upper left", ncol=2)
fig.tight_layout()
