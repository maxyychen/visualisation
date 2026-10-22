# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(30)
# name: (starting level, daily drift %, daily noise %)
kpis = {"Revenue ($k)": (102, 0.6, 1.5), "Orders": (1000, 0.3, 1.5),
        "New users": (980, -0.2, 2.0), "Churn rate (%)": (2.5, 0.3, 1.5),
        "Avg. basket ($)": (66, -0.1, 1.0), "NPS": (40, 0.15, 1.2)}
series = {k: base * np.exp(np.cumsum(rng.normal(d, n, 30)) / 100)
          for k, (base, d, n) in kpis.items()}
df = pd.DataFrame(series)
df.tail()

# %% plot
fig, axes = plt.subplots(len(df.columns), 1, figsize=(5, 4.2))
for ax, col in zip(axes, df.columns):
    s = df[col]
    change = s.iloc[-1] / s.iloc[0] - 1
    ax.plot(s.values, color="#52514e", linewidth=1.2)
    ax.plot(len(s) - 1, s.iloc[-1], "o", color=PALETTE[0], markersize=4)
    ax.fill_between(range(len(s)), s.min(), s.max(), color="#f0efec", linewidth=0)
    ax.axis("off")
    ax.text(-0.05, 0.5, col, transform=ax.transAxes, ha="right", va="center", fontsize=10)
    ax.text(1.05, 0.5, f"{s.iloc[-1]:,.0f}" if s.iloc[-1] >= 100 else f"{s.iloc[-1]:.1f}", transform=ax.transAxes, ha="left",
            va="center", fontsize=10, fontweight="bold")
    ax.text(1.40, 0.5, f"{change:+.1%}", transform=ax.transAxes, ha="left",
            va="center", fontsize=9, color="#52514e")
fig.suptitle("Last 30 days", x=0.02, ha="left", fontweight="bold")
fig.subplots_adjust(left=0.32, right=0.68, hspace=0.6)
