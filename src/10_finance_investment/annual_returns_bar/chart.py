# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.ticker import PercentFormatter

# %% data
rng = np.random.default_rng(21)
dates = pd.bdate_range("2015-01-01", "2024-12-31")
n = len(dates)
mkt = 0.00045 + rng.standard_t(4, n) * 0.0095 / np.sqrt(2)
mkt[(dates >= "2020-02-20") & (dates <= "2020-03-23")] -= 0.012
mkt[(dates >= "2022-01-01") & (dates <= "2022-10-15")] -= 0.0011
fund = 0.00024 + 0.9 * mkt + rng.normal(0, 0.004, n)
daily = pd.DataFrame({"Fund": fund, "Benchmark": mkt}, index=dates)
annual = (1 + daily).groupby(daily.index.year).prod() - 1
annual

# %% plot
fund_name, bench_name = annual.columns[:2]
x = np.arange(len(annual))
excess = annual[fund_name] - annual[bench_name]
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]})
ax.bar(x - 0.2, annual[fund_name], width=0.38, color=PALETTE[0], label=fund_name)
ax.bar(x + 0.2, annual[bench_name], width=0.38, color=GRAY, label=bench_name)
ax.axhline(0, color="#52514e", linewidth=1)
ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
ax.set_ylabel("Calendar-year return")
ax.set_title(f"{fund_name} vs. {bench_name}: calendar-year returns")
ax.legend(loc="upper left", ncol=2)
ax.grid(axis="x", visible=False)

colors = np.where(excess >= 0, PALETTE[0], PALETTE[1])
ax2.bar(x, excess, width=0.55, color=colors)
ax2.axhline(0, color="#52514e", linewidth=1)
for xi, v in zip(x, excess):
    ax2.text(xi, v + (0.002 if v >= 0 else -0.002), f"{v:+.1%}", ha="center",
             va="bottom" if v >= 0 else "top", fontsize=8, color="#52514e")
ax2.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
ax2.set_ylabel("Excess return")
lim = np.abs(excess).max() * 1.6
ax2.set_ylim(-lim, lim)
ax2.set_xticks(x, annual.index)
ax2.grid(axis="x", visible=False)
fig.tight_layout()
