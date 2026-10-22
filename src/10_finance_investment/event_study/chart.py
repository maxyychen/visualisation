# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(31)
n_events, est, win = 160, (-250, -30), np.arange(-10, 11)
beat = rng.random(n_events) < 0.6
rows = []
for e in range(n_events):
    days = np.arange(est[0], win[-1] + 1)
    mkt = rng.normal(0.0004, 0.010, len(days))
    beta_true, alpha_true = rng.uniform(0.7, 1.4), rng.normal(0, 0.0002)
    r = alpha_true + beta_true * mkt + rng.normal(0, 0.010, len(days))
    sign = 1 if beat[e] else -1
    r[days == 0] += sign * (0.025 if beat[e] else 0.030) + rng.normal(0, 0.012)
    r[(days > 0)] += sign * 0.0012                       # post-earnings drift
    r[(days >= -3) & (days < 0)] += sign * 0.0015        # small pre-event run-up
    rows.append(pd.DataFrame({"event": e, "day": days, "ret": r, "mkt": mkt,
                              "group": "Beat" if beat[e] else "Miss"}))
panel = pd.concat(rows, ignore_index=True)
panel.groupby("group")["event"].nunique()

# %% plot
def car_paths(df):
    est_df = df[(df["day"] >= est[0]) & (df["day"] <= est[1])]
    b, a = np.polyfit(est_df["mkt"], est_df["ret"], 1)        # market model
    w = df[df["day"].isin(win)].sort_values("day")
    return (w["ret"] - (a + b * w["mkt"])).cumsum().values

fig, ax = plt.subplots(figsize=(9, 5.2))
for color, (group, g) in zip([PALETTE[0], PALETTE[1]], panel.groupby("group")):
    cars = np.vstack([car_paths(d) for _, d in g.groupby("event")])
    mean = cars.mean(axis=0)
    ci = 1.96 * cars.std(axis=0, ddof=1) / np.sqrt(len(cars))
    ax.fill_between(win, mean - ci, mean + ci, color=color, alpha=0.18, linewidth=0)
    ax.plot(win, mean, color=color, marker="o", markersize=3.5)
    ax.annotate(f"{group}{'es' if group.endswith('s') else 's'} (n={len(cars)})  {mean[-1]:+.1%}", (win[-1], mean[-1]), xytext=(8, 0),
                textcoords="offset points", va="center", color=color, fontsize=10, fontweight="bold")
ax.axhline(0, color="#52514e", linewidth=1)
ax.axvline(0, color="#52514e", linewidth=1)
ax.text(0.3, ax.get_ylim()[1] * 0.92, "Announcement", fontsize=9, color="#52514e")
ax.set_xticks(win[::2])
ax.set_xlim(win[0] - 0.5, win[-1] + 5.5)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:+.0%}"))
ax.set_xlabel("Trading days relative to earnings announcement")
ax.set_ylabel("Mean cumulative abnormal return")
ax.set_title("Earnings surprises: prices jump on the day and keep drifting")
fig.text(0.01, 0.005, "Market-model abnormal returns (estimation window days −250 to −30) · bands = 95% CI of the mean",
         fontsize=8, color="#7a7974")
fig.tight_layout()
