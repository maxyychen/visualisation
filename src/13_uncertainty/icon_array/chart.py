# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.patches import Circle, FancyBboxPatch

# %% data
options = pd.DataFrame({"option": ["Treatment A", "Treatment B"], "affected_per_100": [7, 15]})
options

# %% plot
def person(ax, x, y, color):
    ax.add_patch(Circle((x, y + 0.27), 0.13, color=color, linewidth=0))
    ax.add_patch(FancyBboxPatch((x - 0.16, y - 0.36), 0.32, 0.48,
                                boxstyle="round,pad=0,rounding_size=0.12", color=color, linewidth=0))

fig, axes = plt.subplots(1, 2, figsize=(10, 5.6))
for ax, row in zip(axes, options.itertuples()):
    for k in range(100):
        r, c = divmod(k, 10)
        person(ax, c, 9 - r, PALETTE[1] if k < row.affected_per_100 else "#d0cfca")
    ax.set_xlim(-0.6, 9.6)
    ax.set_ylim(-0.6, 9.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"{row.option}\n{row.affected_per_100} in 100 have a serious side effect",
                 loc="left", fontsize=12)
fig.suptitle("Chance of a serious side effect within one year", x=0.02, ha="left",
             fontsize=13, fontweight="bold")
fig.text(0.02, 0.02, "Orange = side effect   Gray = no side effect   (illustrative numbers)",
         fontsize=9, color="#52514e")
fig.tight_layout(rect=(0, 0.04, 1, 0.92))
