# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(5)
weeks = 104
dates = pd.date_range("2024-01-05", periods=weeks, freq="W-FRI")
t = np.arange(weeks)
bench = 100 * np.exp(np.cumsum(rng.normal(0.002, 0.02, weeks)))
sectors = ["Technology", "Financials", "Health care", "Energy", "Utilities", "Industrials"]
phases = np.linspace(0, 2 * np.pi, len(sectors), endpoint=False)
prices = pd.DataFrame({
    s: bench * np.exp(0.07 * np.sin(2 * np.pi * t / 40 + ph) + np.cumsum(rng.normal(0, 0.004, weeks)))
    for s, ph in zip(sectors, phases)}, index=dates)

rs = prices.div(bench, axis=0)                                   # relative strength
rs_ratio = 100 * rs.ewm(span=6).mean() / rs.ewm(span=26).mean()  # trend of RS
rs_mom = 100 * rs_ratio / rs_ratio.shift(3)                      # rate of change of that trend
rs_ratio.tail(3).round(2)

# %% plot
tail = 8
r, m = rs_ratio.iloc[-tail:], rs_mom.iloc[-tail:]
dx = (r - 100).abs().to_numpy().max() * 1.3
dy = (m - 100).abs().to_numpy().max() * 1.3

fig, ax = plt.subplots(figsize=(8.5, 7.5))
quads = [((100, 100), "Leading", "#e4eefb", (1, 1)), ((100 - dx, 100), "Improving", "#ebe8fa", (-1, 1)),
         ((100 - dx, 100 - dy), "Lagging", "#fbe6dc", (-1, -1)), ((100, 100 - dy), "Weakening", "#fbf1d9", (1, -1))]
for (x0, y0), name, tint, (sx, sy) in quads:
    ax.add_patch(plt.Rectangle((x0, y0), dx, dy, facecolor=tint, linewidth=0, zorder=0))
    ax.text(100 + sx * dx * 0.97, 100 + sy * dy * 0.95, name, ha="right" if sx > 0 else "left",
            va="top" if sy > 0 else "bottom", fontsize=11, fontweight="bold", color="#52514e")
ax.axhline(100, color="#a9a8a2", linewidth=0.8)
ax.axvline(100, color="#a9a8a2", linewidth=0.8)

for s in sectors:
    ax.plot(r[s], m[s], color="#52514e", linewidth=1.2, zorder=2)
    ax.scatter(r[s].iloc[:-1], m[s].iloc[:-1], s=np.linspace(6, 22, tail - 1), color="#52514e", zorder=3)
    ax.scatter(r[s].iloc[-1], m[s].iloc[-1], s=90, color=PALETTE[0], edgecolor="#fcfcfb",
               linewidth=2, zorder=4)
    ax.annotate(s, (r[s].iloc[-1], m[s].iloc[-1]), xytext=(7, 5), textcoords="offset points",
                fontsize=9.5, fontweight="bold", zorder=5)

ax.set_xlim(100 - dx, 100 + dx)
ax.set_ylim(100 - dy, 100 + dy)
ax.grid(False)
ax.set_xlabel("RS-ratio (relative strength vs benchmark) →")
ax.set_ylabel("RS-momentum (change in relative strength) →")
ax.set_title(f"Sector rotation: last {tail} weeks (simulated)")
fig.tight_layout()
