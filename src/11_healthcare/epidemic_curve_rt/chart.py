# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from vizlib.health import epicurve, discretised_serial_interval, estimate_rt

# %% data
rng = np.random.default_rng(2013)
days, intervention = 110, 40
dates = pd.date_range("2025-02-01", periods=days, freq="D")
serial_interval = discretised_serial_interval(mean=4.7, sd=2.9, max_days=20)
# True R: 1.6 until the measures, then ~0.75, with a one-week transition.
step = np.where(np.arange(days) < intervention, 1.6, 0.75)
true_r = np.convolve(np.r_[np.full(6, step[0]), step], np.ones(7) / 7, mode="valid")
cases = np.zeros(days, dtype=int)
cases[:5] = [3, 2, 4, 3, 5]
for t in range(5, days):                      # renewal process: new cases ~ Poisson(R * infectiousness)
    pressure = np.dot(cases[max(0, t - 20):t][::-1], serial_interval[:min(t, 20)])
    cases[t] = rng.poisson(true_r[t] * pressure)
onset = np.repeat(dates, cases)
confirmed = rng.random(onset.size) < 0.7
curve = pd.DataFrame({
    "confirmed": epicurve(onset[confirmed], start=dates[0], end=dates[-1]),
    "probable": epicurve(onset[~confirmed], start=dates[0], end=dates[-1]),
})
rt = estimate_rt(curve.sum(axis=1), serial_interval, window=7).loc[dates[10]:]
curve.assign(total=curve.sum(axis=1)).describe().round(0)

# %% plot
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [1.3, 1]})
a1.bar(curve.index, curve["confirmed"], width=0.9, color=PALETTE[0], label="Confirmed")
a1.bar(curve.index, curve["probable"], bottom=curve["confirmed"], width=0.9, color="#86b6ef", label="Probable")
a1.set_ylabel("New cases by onset date")
a1.set_ylim(0, curve.sum(axis=1).max() * 1.35)
a1.set_title("Epidemic curve", fontsize=11)
a1.legend(loc="upper right")
a1.grid(axis="x", visible=False)
a2.fill_between(rt.index, rt["lower"], rt["upper"], color=PALETTE[0], alpha=0.25, linewidth=0,
                label="95% credible interval")
a2.plot(rt.index, rt["rt"], color=PALETTE[0], linewidth=2, label="Estimated Rt")
a2.plot(dates, true_r, color="#8f8e88", linewidth=1, label="True Rt (simulation)")
a2.axhline(1, color="#52514e", linewidth=1.2)
a2.text(dates[-1], 1.03, "Rt = 1: growth above, decline below", ha="right", va="bottom", fontsize=8.5,
        color="#52514e")
a2.set_ylim(0, 2.6)
a2.set_ylabel("Reproduction number Rt")
a2.set_title("Time-varying reproduction number (Cori et al., 7-day window)", fontsize=11)
a2.legend(loc="upper right", fontsize=8.5)
for ax in (a1, a2):
    ax.axvline(dates[intervention], color="#52514e", linewidth=1)
a1.annotate("Distancing measures start (day 40)", (dates[intervention], a1.get_ylim()[1]), xytext=(-6, -4),
            textcoords="offset points", ha="right", va="top", fontsize=8.5)
a2.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%d %b"))
fig.suptitle("The outbreak peaked after the measures, but Rt fell below 1 eight days later (simulated)",
             x=0.01, ha="left", fontweight="bold", fontsize=12.5)
fig.tight_layout()
