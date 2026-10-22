# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(21)
n_total, n_show = 170, 120          # extra history warms up the 50-day average
dates = pd.bdate_range("2025-01-02", periods=n_total)
ret = rng.normal(0.0006, 0.016, n_total)
ret[95:115] += 0.004                # a rally
ret[140:152] -= 0.007               # a pullback
close = 80 * np.exp(np.cumsum(ret))
open_ = np.r_[80, close[:-1]] * (1 + rng.normal(0, 0.004, n_total))
high = np.maximum(open_, close) * (1 + rng.uniform(0.001, 0.014, n_total))
low = np.minimum(open_, close) * (1 - rng.uniform(0.001, 0.014, n_total))
volume = rng.lognormal(np.log(2e6), 0.3, n_total) * (1 + 10 * np.abs(ret))

df = pd.DataFrame({"open": open_, "high": high, "low": low, "close": close,
                   "volume": volume}, index=dates)
df["ma20"] = df["close"].rolling(20).mean()
df["ma50"] = df["close"].rolling(50).mean()
sd20 = df["close"].rolling(20).std()
df["bb_upper"] = df["ma20"] + 2 * sd20
df["bb_lower"] = df["ma20"] - 2 * sd20
df["vol_ma20"] = df["volume"].rolling(20).mean()
df = df.iloc[-n_show:].round(2)
df.tail()

# %% plot
fig, (ax, axv) = plt.subplots(2, 1, figsize=(11, 6.8), sharex=True,
                              gridspec_kw={"height_ratios": [3.2, 1]})
x = np.arange(len(df))
up = (df["close"] >= df["open"]).to_numpy()
colors = np.where(up, PALETTE[0], PALETTE[1])

ax.fill_between(x, df["bb_lower"], df["bb_upper"], color="#dddcd6", alpha=0.7, linewidth=0)
ax.vlines(x, df["low"], df["high"], color=colors, linewidth=0.9)
ax.bar(x, (df["close"] - df["open"]).abs().clip(lower=0.03),
       bottom=df[["open", "close"]].min(axis=1), color=colors, width=0.7)
ax.plot(x, df["ma20"], color=PALETTE[6], linewidth=1.5)
ax.plot(x, df["ma50"], color="#0b0b0b", linewidth=1.5)
end = len(df) - 1
for col, label, color in [("ma20", "20-day MA", PALETTE[6]), ("ma50", "50-day MA", "#0b0b0b")]:
    ax.text(end + 1.5, df[col].iloc[-1], label, color=color, va="center", fontsize=9)
ax.text(end + 1.5, df["bb_upper"].iloc[-1], "Bollinger\n(±2σ)", color="#7a7974",
        va="bottom", fontsize=8.5)
ax.set_xlim(-1, len(df) + 11)
ax.set_ylabel("Price ($)")
ax.set_title("ACME Corp.: price, trend and volatility (simulated)")

axv.bar(x, df["volume"] / 1e6, color=colors, width=0.7, alpha=0.55)
axv.plot(x, df["vol_ma20"] / 1e6, color="#52514e", linewidth=1.2)
axv.text(end + 1.5, df["vol_ma20"].iloc[-1] / 1e6, "20-day avg", color="#52514e",
         va="center", fontsize=8.5)
axv.set_ylabel("Volume (M)")

month_start = np.flatnonzero(df.index.month != np.r_[0, df.index.month[:-1]])
axv.set_xticks(month_start, df.index[month_start].strftime("%b %Y"))
for a in (ax, axv):
    a.grid(axis="x", visible=False)
fig.tight_layout()
