# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from vizlib.health import run_chart_signals

# %% data
rng = np.random.default_rng(2011)
months = pd.period_range("2023-01", periods=30, freq="M")
baseline = 72 + rng.normal(0, 2.2, 15)
ramp = np.array([74.5, 77.0, 79.5, 82.0, 84.0])
after = 85 + rng.normal(0, 1.6, 10)
df = pd.DataFrame({"month": months.to_timestamp(), "compliance": np.r_[baseline, ramp, after].round(1)})
change = 15  # index of the first month with the new programme
baseline_median = float(np.median(df["compliance"].iloc[:change]))
signals = run_chart_signals(df["compliance"], center=baseline_median)
{k: signals[k] for k in ("median", "shift", "trend", "runs", "runs_expected")}

# %% plot
fig, ax = plt.subplots(figsize=(10, 5))
x, y = df["month"], df["compliance"]
ax.plot(x, y, color="#8f8e88", linewidth=1.5, marker="o", markersize=5, zorder=2)
ax.axhline(signals["median"], color="#52514e", linewidth=1)
ax.text(x.iloc[0], 65.2, f"Horizontal line: baseline median {signals['median']:.1f}%\n(months 1–15, frozen and extended)",
        fontsize=9, color="#52514e", va="bottom")
shift, trend = signals["shift"], signals["trend"]
ax.scatter(x.iloc[shift], y.iloc[shift], s=70, color=PALETTE[1], edgecolor="#fcfcfb", linewidth=1.5,
           zorder=4, label=f"Shift: {len(shift)} points above the median")
ax.scatter(x.iloc[trend], y.iloc[trend], s=120, marker="^", facecolor="none", edgecolor=PALETTE[1],
           linewidth=1.6, zorder=5, label=f"Trend: {len(trend)} points rising in a row")
ax.axvline(x.iloc[change], color="#52514e", linewidth=1)
ax.annotate("New dispensers + monthly\nfeedback start", (x.iloc[change], 90.5), xytext=(8, 0),
            textcoords="offset points", fontsize=9, va="top")
ax.set_ylim(64, 91)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.set_ylabel("Hand-hygiene compliance (audited)")
ax.set_title("Ward 7 hand-hygiene compliance: the programme shifted the process (simulated)")
ax.legend(loc="lower right")
fig.tight_layout()
