# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from vizlib.health import p_chart, u_chart, run_chart_signals

# %% data
rng = np.random.default_rng(2008)
months = pd.period_range("2022-01", periods=36, freq="M").to_timestamp()
operations = rng.integers(80, 221, 36)
ssi_rate = np.full(36, 0.035)
ssi_rate[19] = 0.12                      # outbreak month
infections = rng.binomial(operations, ssi_rate)
bed_days = rng.integers(2500, 3301, 36)
falls_rate = np.where(np.arange(36) < 27, 4.0, 1.9) / 1000
falls = rng.poisson(falls_rate * bed_days)
change = 27                          # falls bundle starts (month 28)
p = p_chart(infections, operations)
# Freeze the u-chart centre on the baseline months, then extend its limits to every month.
ubar = u_chart(falls[:change], bed_days[:change])["center"].iloc[0]
u = pd.DataFrame({"u": falls / bed_days, "center": ubar})
u["ucl"] = ubar + 3 * np.sqrt(ubar / bed_days)
u["lcl"] = np.clip(ubar - 3 * np.sqrt(ubar / bed_days), 0, None)
u["signal"] = (u["u"] > u["ucl"]) | (u["u"] < u["lcl"])
falls_shift = run_chart_signals(u["u"], center=ubar, shift=8)["shift"]   # rule: 8+ points below centre
pd.DataFrame({"month": months, "operations": operations, "infections": infections,
              "bed_days": bed_days, "falls": falls}).head()

# %% plot
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
for ax, chart, value, scale, label in (
        (a1, p, "p", 100, "Surgical-site infections (% of operations)"),
        (a2, u, "u", 1000, "Falls per 1,000 bed-days")):
    v = chart[value] * scale
    ax.step(months, chart["ucl"] * scale, where="mid", color="#b8b7b1", linewidth=1.2)
    ax.step(months, chart["lcl"] * scale, where="mid", color="#b8b7b1", linewidth=1.2)
    ax.hlines(chart["center"].iloc[0] * scale, months[0], months[-1], color="#52514e", linewidth=1)
    ax.plot(months, v, color=PALETTE[0], marker="o", markersize=4.5, linewidth=1.5, zorder=3)
    sig = chart["signal"].values
    ax.scatter(months[sig], v[sig], s=80, color=PALETTE[1], edgecolor="#fcfcfb", linewidth=1.5, zorder=4)
    for m, val in zip(months[sig], v[sig]):
        ax.annotate("signal", (m, val), xytext=(6, 4), textcoords="offset points", fontsize=8.5,
                    color="#0b0b0b")
    label_x = months[-1] + np.timedelta64(20, "D")
    for key, text in (("center", "centre"), ("ucl", "UCL"), ("lcl", "LCL")):
        ax.text(label_x, chart[key].iloc[-1] * scale, text, va="center", fontsize=8.5, color="#52514e")
    ax.set_ylabel(label)
    ax.set_ylim(0, max(chart["ucl"].max() * scale, v.max()) * 1.15)
    ax.set_xlim(months[0] - np.timedelta64(20, "D"), months[-1] + np.timedelta64(75, "D"))
a1.set_title("p-chart: one infection month is a special cause", fontsize=11)
a2.set_title("u-chart (limits frozen on the 27 baseline months): the falls bundle shifted the process", fontsize=11)
a2.scatter(months[falls_shift], u["u"].values[falls_shift] * 1000, s=110, marker="v", facecolor="none",
           edgecolor=PALETTE[1], linewidth=1.6, zorder=5)
a2.text(months[31], ubar * 1000 * 1.35, f"▽ shift rule: {len(falls_shift)} months\nbelow the baseline centre",
        ha="center", va="bottom", fontsize=8.5)
a2.axvline(months[change], color="#52514e", linewidth=1)
a2.annotate("Falls-prevention\nbundle starts", (months[change], a2.get_ylim()[1]), xytext=(-6, -2),
            textcoords="offset points", fontsize=8.5, ha="right", va="top",
            bbox=dict(boxstyle="square,pad=0.15", fc="#fcfcfb", ec="none"))
fig.suptitle("Hospital safety indicators with 3-sigma control limits (simulated)", x=0.01, ha="left",
             fontweight="bold", fontsize=13)
fig.tight_layout()
