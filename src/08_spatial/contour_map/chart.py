# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(4)
x = np.linspace(0, 100, 220); y = np.linspace(0, 80, 180)
X, Y = np.meshgrid(x, y)
def bump(cx, cy, sx, sy, h):
    return h * np.exp(-(((X - cx) / sx) ** 2 + ((Y - cy) / sy) ** 2))
Z = (900 + bump(30, 55, 18, 10, 1600) + bump(75, 25, 12, 16, 1100)
     + bump(55, 70, 25, 8, 500) - 4 * X)
towns = pd.DataFrame({"town": ["Ashford", "Brook", "Calder", "Dunmore", "Elm"],
                      "x": [12, 48, 85, 62, 20], "y": [20, 40, 60, 8, 70]})
towns

# %% plot
fig, ax = plt.subplots(figsize=(9, 6.2))
levels = np.arange(400, 2700, 250)
cf = ax.contourf(X, Y, Z, levels=levels, cmap=SEQ_CMAP, extend="both")
cs = ax.contour(X, Y, Z, levels=levels[::2], colors="#52514e", linewidths=0.6)
ax.clabel(cs, fmt="%d", fontsize=8)
ax.scatter(towns.x, towns.y, s=40, color=PALETTE[1], edgecolor="#fcfcfb", linewidth=1.5, zorder=3)
for _, t in towns.iterrows():
    ax.annotate(t.town, (t.x, t.y), xytext=(6, 4), textcoords="offset points", fontsize=9,
                fontweight="bold", color="#0b0b0b")
cb = fig.colorbar(cf, ax=ax, shrink=0.85); cb.set_label("Annual rainfall (mm)")
cb.outline.set_visible(False)
ax.set_xlabel("km east"); ax.set_ylabel("km north"); ax.set_aspect("equal")
ax.grid(False)
ax.set_title("Annual rainfall (synthetic)")
fig.tight_layout()
