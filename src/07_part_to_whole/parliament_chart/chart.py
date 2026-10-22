# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
seats = pd.Series({"Party A": 52, "Party B": 38, "Party C": 14, "Party D": 8, "Other": 8})
assert seats.sum() == 120
seats

# %% plot
n_rows, total = 6, seats.sum()
radii = np.linspace(1.0, 2.0, n_rows)
per_row = np.round(radii / radii.sum() * total).astype(int)
per_row[-1] += total - per_row.sum()
pts = []
for r, n in zip(radii, per_row):
    for a in np.linspace(np.pi, 0, n):
        pts.append((a, r * np.cos(a), r * np.sin(a)))
pts.sort(key=lambda p: -p[0])           # fill left to right by angle
colors = PALETTE[:len(seats) - 1] + [GRAY]
seat_colors = np.repeat(colors, seats.values)
fig, ax = plt.subplots(figsize=(9, 5))
xs, ys = [p[1] for p in pts], [p[2] for p in pts]
ax.scatter(xs, ys, c=seat_colors, s=95, edgecolor="#fcfcfb", linewidth=1.5)
ax.text(0, 0.15, f"{total} seats\nmajority = {total // 2 + 1}", ha="center",
        fontsize=12, fontweight="bold")
ax.set_aspect("equal")
ax.axis("off")
handles = [plt.Line2D([], [], marker="o", ls="", color=c, markersize=9) for c in colors]
ax.legend(handles, [f"{k} ({v})" for k, v in seats.items()], ncol=5,
          loc="upper center", bbox_to_anchor=(0.5, 0.02))
ax.set_title("Parliament seat allocation")
fig.tight_layout()
