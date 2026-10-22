# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(4)
regions = ["North", "South", "East", "West", "Central", "Coast"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
base = np.array([62, 55, 38, 58, 50, 45], dtype=float)
sales = base + rng.normal(0, 4, (12, 6))
sales[:, 2] += np.linspace(0, 30, 12)                  # East grows steadily
df = pd.DataFrame(sales.round(1), index=months, columns=regions)
df.iloc[[0, 6, 11]]

# %% plot
fig = plt.figure(figsize=(13, 5.4))
left, right = fig.subfigures(1, 2, width_ratios=[1, 1.5], wspace=0.04)

# Left: one frame of the animation, with a player bar.
ax = left.subplots()
frame = 6
ax.bar(regions, df.iloc[frame], color=PALETTE[:6], width=0.7)
ax.set_ylim(0, 85)
ax.set_ylabel("Sales (US$ k)")
ax.grid(axis="x", visible=False)
ax.set_title("✗ Misleading: animation (frame 7 of 12)", loc="left", fontsize=12)
ax.text(0.98, 0.95, months[frame], transform=ax.transAxes, ha="right", va="top",
        fontsize=26, fontweight="bold", color="#d0cfca")
ax.annotate("", xy=(1, -0.16), xytext=(0, -0.16), xycoords="axes fraction",
            arrowprops=dict(arrowstyle="-", color="#d0cfca", linewidth=6))
ax.annotate("", xy=((frame + 1) / 12, -0.16), xytext=(0, -0.16), xycoords="axes fraction",
            arrowprops=dict(arrowstyle="-", color=PALETTE[0], linewidth=6))
ax.text(0, -0.24, "▶  Was East higher in March? You have to remember.", transform=ax.transAxes,
        fontsize=9, color="#52514e")

# Right: small multiples with shared axes, East highlighted.
right.suptitle("✓ Better: small multiples: every month at once", x=0.02, ha="left",
               fontsize=12, fontweight="bold")
axes = right.subplots(2, 6, sharex=True, sharey=True)
colors = [PALETTE[0] if r == "East" else GRAY for r in regions]
for ax, month in zip(axes.flat, months):
    ax.bar(range(6), df.loc[month], color=colors, width=0.75)
    ax.set_title(month, fontsize=9, fontweight="normal")
    ax.set_xticks([2], ["East"], fontsize=8)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="x", visible=False)
    ax.set_ylim(0, 85)
axes[0, 0].set_ylabel("Sales ($k)", fontsize=8)
axes[1, 0].set_ylabel("Sales ($k)", fontsize=8)
