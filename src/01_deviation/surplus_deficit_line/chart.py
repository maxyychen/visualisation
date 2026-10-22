# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(3)
dates = pd.date_range("2015-01", periods=120, freq="MS")
trend = np.linspace(-0.3, 0.6, len(dates))
anomaly = trend + 0.35 * np.sin(np.arange(len(dates)) / 6) + rng.normal(0, 0.15, len(dates))
df = pd.DataFrame({"date": dates, "anomaly": anomaly})
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(9, 4.5))
x, y = df["date"], df["anomaly"]
ax.fill_between(x, y, 0, where=y >= 0, interpolate=True, color=PALETTE[7], alpha=0.75, label="Warmer")
ax.fill_between(x, y, 0, where=y < 0, interpolate=True, color=PALETTE[0], alpha=0.75, label="Cooler")
ax.plot(x, y, color="#52514e", linewidth=0.8)
ax.axhline(0, color="#52514e", linewidth=1)
ax.set_ylabel("Anomaly (°C)")
ax.set_title("Monthly temperature anomaly vs. 1991–2020 average")
ax.legend(loc="upper left")
fig.tight_layout()
