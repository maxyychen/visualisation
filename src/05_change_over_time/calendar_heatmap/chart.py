# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(15)
days = pd.date_range("2025-01-01", "2025-12-31", freq="D")
weekend = days.dayofweek >= 5
minutes = rng.gamma(2, 15, len(days)) + np.where(weekend, 25, 0) \
    + 15 * np.sin((days.dayofyear.values - 80) / 365 * 2 * np.pi)
minutes[rng.random(len(days)) < 0.12] = 0
df = pd.DataFrame({"date": days, "minutes": minutes.clip(0).round()})
df["week"] = ((df["date"] - pd.Timestamp("2024-12-30")).dt.days // 7)
df["weekday"] = df["date"].dt.dayofweek
df.head()

# %% plot
grid = df.pivot(index="weekday", columns="week", values="minutes")
fig, ax = plt.subplots(figsize=(12, 2.8))
mesh = ax.pcolormesh(grid.columns, grid.index, grid.values, cmap=SEQ_CMAP,
                     edgecolors="#fcfcfb", linewidth=1.5, shading="nearest")
ax.set_aspect("equal")
ax.invert_yaxis()
ax.set_yticks(range(7), ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], fontsize=8)
month_starts = df[df["date"].dt.day == 1]
ax.set_xticks(month_starts["week"], month_starts["date"].dt.strftime("%b"), fontsize=8)
ax.grid(False)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)
fig.colorbar(mesh, ax=ax, shrink=0.8, pad=0.01, label="Minutes")
ax.set_title("Daily exercise minutes, 2025")
fig.tight_layout()
