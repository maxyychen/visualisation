# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
regions = ["North", "East", "South", "West", "Central"]
mix = pd.DataFrame({
    "Coal":    [35, 20, 45, 10, 28],
    "Gas":     [30, 35, 25, 30, 32],
    "Nuclear": [15, 25,  5, 10, 20],
    "Renewables": [20, 20, 25, 50, 20],
}, index=regions)
share = mix.div(mix.sum(axis=1), axis=0) * 100
share = share.sort_values("Renewables")
share.round(1)

# %% plot
fig, ax = plt.subplots(figsize=(9, 4.5))
left = np.zeros(len(share))
for i, col in enumerate(share.columns):
    vals = share[col].values
    ax.barh(share.index, vals, left=left, color=PALETTE[i], label=col,
            height=0.65, edgecolor="#fcfcfb", linewidth=2)
    for y, (l, v) in enumerate(zip(left, vals)):
        if v >= 8:
            ax.text(l + v / 2, y, f"{v:.0f}%", ha="center", va="center",
                    fontsize=9, color="white", fontweight="bold")
    left += vals
ax.set_xlim(0, 100)
ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0f}%")
ax.set_title("Electricity generation mix by region")
ax.grid(axis="y", visible=False)
ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.1))
fig.tight_layout()
