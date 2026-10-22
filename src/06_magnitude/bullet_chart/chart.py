# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame([
    ("Revenue ($M)", 270, 250, [150, 225, 300]),
    ("Profit (%)", 22.5, 26, [20, 25, 30]),
    ("Avg. order ($)", 320, 550, [350, 500, 600]),
    ("New customers", 1650, 2100, [1400, 2000, 2500]),
    ("Satisfaction (1–5)", 4.5, 4.2, [3.5, 4.25, 5]),
], columns=["kpi", "actual", "target", "ranges"])
df

# %% plot
fig, axes = plt.subplots(len(df), 1, figsize=(8, 4.5))
band_colors = ["#d6d5d0", "#e6e5e1", "#f3f2ef"]
for ax, (_, r) in zip(axes, df.iterrows()):
    prev = 0
    for upper, c in zip(r["ranges"], band_colors):
        ax.barh(0, upper - prev, left=prev, color=c, height=1)
        prev = upper
    ax.barh(0, r["actual"], color=PALETTE[0] if r["actual"] >= r["target"] else PALETTE[1],
            height=0.35)
    ax.vlines(r["target"], -0.35, 0.35, color="#0b0b0b", linewidth=2.5)
    ax.set_xlim(0, r["ranges"][-1])
    ax.set_yticks([0], [r["kpi"]])
    ax.grid(False)
    ax.tick_params(axis="x", labelsize=8)
    for s in ["left", "bottom"]:
        ax.spines[s].set_visible(False)
fig.suptitle("KPI scorecard (bar = actual, tick = target; orange = below target)",
             x=0.02, ha="left", fontweight="bold")
fig.tight_layout()
