# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from vizlib.health import reference_flags
import matplotlib.dates as mdates

# %% data
rng = np.random.default_rng(410)
dates = pd.date_range("2024-01-15", periods=13, freq="28D")
m = np.arange(len(dates))
after = 1 / (1 + np.exp(-(m - 5) * 1.5))            # effect of a medication change around month 5
labs = {  # test: (units, low, high, values)
    "Creatinine": ("mg/dL", 0.6, 1.3, 1.9 - 0.65 * after + rng.normal(0, 0.06, m.size)),
    "Potassium": ("mmol/L", 3.5, 5.1, 5.7 - 0.9 * after + rng.normal(0, 0.12, m.size)),
    "Haemoglobin": ("g/dL", 12.0, 16.0, 10.6 + 0.6 * after + rng.normal(0, 0.25, m.size)),
    "Sodium": ("mmol/L", 135, 145, 140 + rng.normal(0, 1.0, m.size)),
    "Glucose (fasting)": ("mg/dL", 70, 100, 86 + rng.normal(0, 2.5, m.size) + 30 * (m == 8)),
}
records = pd.DataFrame([
    dict(test=t, units=u, low=lo, high=hi, date=d, value=round(float(v), 2))
    for t, (u, lo, hi, vals) in labs.items() for d, v in zip(dates, vals)])
records["flag"] = np.concatenate([reference_flags(g["value"], g["low"].iloc[0], g["high"].iloc[0])
                                  for _, g in records.groupby("test", sort=False)])
records[records["flag"] != ""].head()

# %% plot
tests = list(labs)
fig, axes = plt.subplots(len(tests), 1, figsize=(9, 9), sharex=True)
for ax, test in zip(axes, tests):
    g = records[records["test"] == test]
    lo, hi, units = g["low"].iloc[0], g["high"].iloc[0], g["units"].iloc[0]
    ax.axhspan(lo, hi, color=PALETTE[2], alpha=0.13, linewidth=0)
    ax.plot(g["date"], g["value"], "-", color="#8f8e88", linewidth=1.2)
    normal, out = g[g["flag"] == ""], g[g["flag"] != ""]
    ax.plot(normal["date"], normal["value"], "o", color=PALETTE[0], markersize=5)
    ax.plot(out["date"], out["value"], "o", color=PALETTE[1], markersize=6)
    for _, r in out.iterrows():
        ax.annotate(r["flag"], (r["date"], r["value"]), xytext=(0, 6 if r["flag"] == "H" else -12),
                    textcoords="offset points", ha="center", fontsize=8, fontweight="bold", color="#0b0b0b")
    span = max(g["value"].max(), hi) - min(g["value"].min(), lo)
    ax.set_ylim(min(g["value"].min(), lo) - 0.25 * span, max(g["value"].max(), hi) + 0.3 * span)
    ax.set_title(f"{test} ({units}) · reference {lo:g}–{hi:g}", fontsize=10, loc="left")
    ax.grid(axis="x", visible=False)
axes[-1].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
fig.suptitle("Lab results vs. reference ranges (simulated patient) · H = high, L = low",
             x=0.02, ha="left", fontsize=13, fontweight="bold")
fig.tight_layout()
