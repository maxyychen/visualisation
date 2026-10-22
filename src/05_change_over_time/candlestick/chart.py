# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(42)
n = 60
dates = pd.bdate_range("2025-03-03", periods=n)
close = 100 * np.exp(np.cumsum(rng.normal(0.001, 0.018, n)))
open_ = np.r_[100, close[:-1]] * (1 + rng.normal(0, 0.005, n))
high = np.maximum(open_, close) * (1 + rng.uniform(0.002, 0.02, n))
low = np.minimum(open_, close) * (1 - rng.uniform(0.002, 0.02, n))
volume = rng.integers(8e5, 3e6, n)
df = pd.DataFrame({"open": open_, "high": high, "low": low, "close": close,
                   "volume": volume}, index=dates).round(2)
df.head()

# %% plot
up_color, down_color = PALETTE[0], PALETTE[1]
fig, (ax, axv) = plt.subplots(2, 1, figsize=(10, 6), sharex=True,
                              gridspec_kw={"height_ratios": [3, 1]})
x = np.arange(len(df))
up = df["close"] >= df["open"]
colors = np.where(up, up_color, down_color)
ax.vlines(x, df["low"], df["high"], color=colors, linewidth=1)
ax.bar(x, (df["close"] - df["open"]).abs(), bottom=df[["open", "close"]].min(axis=1),
       color=colors, width=0.65)
axv.bar(x, df["volume"] / 1e6, color=colors, width=0.65, alpha=0.6)
ax.set_ylabel("Price ($)")
axv.set_ylabel("Volume (M)")
ticks = x[::10]
axv.set_xticks(ticks, df.index[::10].strftime("%b %d"))
ax.grid(axis="x", visible=False)
axv.grid(axis="x", visible=False)
ax.set_title("ACME Corp. daily price (blue = close above open)")
fig.tight_layout()
