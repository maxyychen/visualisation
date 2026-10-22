# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(3)
tiles = [
    ("Monthly revenue", "$1.24M", "+8.2% vs last month", True, np.cumsum(rng.normal(1, 1, 12))),
    ("Active users", "48.9k", "+3.1% vs last month", True, np.cumsum(rng.normal(.5, 1, 12))),
    ("Churn rate", "2.7%", "+0.4 pts vs last month", False, np.cumsum(rng.normal(.3, 1, 12))),
    ("Support tickets", "312", "−12% vs last month", True, np.cumsum(rng.normal(-.5, 1, 12))),
]
pd.DataFrame(tiles, columns=["label", "value", "delta", "good", "trend"]).drop(columns="trend")

# %% plot
fig, axes = plt.subplots(1, 4, figsize=(11, 2.8))
for ax, (label, value, delta, good, trend) in zip(axes, tiles):
    ax.set_facecolor("#f3f2ef")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    ax.text(0.07, 0.83, label, transform=ax.transAxes, fontsize=12, color="#52514e")
    ax.text(0.07, 0.48, value, transform=ax.transAxes, fontsize=30, fontweight="bold")
    arrow = "▲" if delta.startswith("+") else "▼"
    ax.text(0.07, 0.24, f"{arrow} {delta}", transform=ax.transAxes, fontsize=10.5,
            color="#008300" if good else "#c4462b")
    ins = ax.inset_axes([0.07, 0.03, 0.86, 0.14])
    ins.plot(trend, color="#8c8b86", linewidth=1)
    ins.plot(len(trend) - 1, trend[-1], "o", color=PALETTE[0], markersize=3)
    ins.axis("off")
fig.tight_layout(w_pad=1.5)
