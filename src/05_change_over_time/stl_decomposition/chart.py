# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from statsmodels.tsa.seasonal import STL

# %% data
rng = np.random.default_rng(4)
idx = pd.date_range("2010-01-01", "2024-12-01", freq="MS")
t = np.arange(len(idx))
trend = 300 + 1.1 * np.minimum(t, 110) + 0.15 * np.maximum(t - 110, 0)
amp_summer = 25 + 0.12 * t
season = amp_summer * np.exp(-((idx.month - 7.5) / 1.3) ** 2) + 20 * np.exp(-((idx.month % 12 - 0.5) / 1.4) ** 2)
noise = rng.normal(0, 4, len(idx))
shock = np.zeros(len(idx))
shock[(idx >= "2020-04-01") & (idx <= "2020-06-01")] = -28      # lockdown dip
shock[idx == "2022-07-01"] = 30                                   # heat wave
demand = pd.Series(trend + season + noise + shock, index=idx, name="demand (GWh)")
demand.tail(6).round(1)

# %% plot
res = STL(demand, period=12, robust=True).fit()
parts = [("Observed", demand), ("Trend", res.trend), ("Seasonal", res.seasonal), ("Residual", res.resid)]
fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True,
                         gridspec_kw={"height_ratios": [1.4, 1, 1, 0.9], "hspace": 0.18})
for ax, (name, s) in zip(axes, parts):
    if name == "Residual":
        big = s.abs() > 3 * s.std()
        ax.bar(s.index, s, width=25, color=np.where(big, PALETTE[1], "#b8b7b1"))
        ax.axhline(0, color="#52514e", linewidth=0.8)
        for d, v in (s[big].nlargest(1).items() if (s[big] > 0).any() else []):
            ax.annotate(f"{d:%b %Y}", (d, v), xytext=(4, 0), textcoords="offset points",
                        fontsize=8, color="#52514e", va="bottom")
        for d, v in (s[big].nsmallest(1).items() if (s[big] < 0).any() else []):
            ax.annotate(f"{d:%b %Y}", (d, v), xytext=(4, 0), textcoords="offset points",
                        fontsize=8, color="#52514e", va="top")
    else:
        ax.plot(s.index, s, color="#0b0b0b" if name == "Observed" else PALETTE[0],
                linewidth=1.3 if name != "Trend" else 2)
    ax.text(0.005, 0.92, name, transform=ax.transAxes, fontsize=10, fontweight="bold", va="top")
    ax.set_ylabel("GWh", fontsize=9)
axes[0].set_title("Monthly electricity demand, decomposed with STL (simulated)")
fig.align_ylabels(axes)
