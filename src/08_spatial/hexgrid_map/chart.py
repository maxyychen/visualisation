# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.colors import LogNorm

# %% data
rng = np.random.default_rng(31)


def coast_x(y):
    """x position (km) of the coastline at height y; the sea lies to the east."""
    return 31 + 3 * np.sin(y / 4.5) + 1.5 * np.sin(y / 1.7)


centres = {  # name: (x, y, spread km, share of transactions)
    "Downtown": (27.5, 15, 2.2, 0.38), "North suburb": (18, 25, 2.5, 0.12),
    "West suburb": (8, 13, 2.8, 0.12), "South suburb": (17, 5, 2.4, 0.10),
    "Harbour Mall": (24, 22, 0.8, 0.07), "Ring Mall": (12, 19, 0.8, 0.06),
}
pts = []
for x, y, s, share in centres.values():
    k = int(share * 60000)
    pts.append(np.column_stack([rng.normal(x, s, k), rng.normal(y, s, k)]))
k = int(0.15 * 60000)
pts.append(np.column_stack([rng.uniform(0, 40, k), rng.uniform(0, 30, k)]))
pts = np.vstack(pts)
on_land = (pts[:, 0] > 0) & (pts[:, 1] > 0) & (pts[:, 1] < 30) & (pts[:, 0] < coast_x(pts[:, 1]))
df = pd.DataFrame(pts[on_land][:50000], columns=["x_km", "y_km"])
print(f"{len(df):,} transactions")

# %% plot
fig, ax = plt.subplots(figsize=(9, 6.6))
yy = np.linspace(0, 30, 300)
ax.fill_betweenx(yy, coast_x(yy), 40, color="#ecebe7", zorder=0)
ax.plot(coast_x(yy), yy, color="#b8b7b1", linewidth=1)
ax.text(37, 27.5, "Sea", color="#8f8e88", fontsize=10, style="italic", ha="center")
hb = ax.hexbin(df["x_km"], df["y_km"], gridsize=(42, 18), extent=(0, 40, 0, 30), mincnt=1,
               cmap=SEQ_CMAP, norm=LogNorm(), linewidths=0.3, edgecolors="#fcfcfb")
for name, (x, y, s, share) in centres.items():
    ax.annotate(name, (x, y), xytext=(x - 4.5 if name == "Downtown" else x, y + s + 1.2),
                ha="center", fontsize=8.5, color="#0b0b0b",
                bbox=dict(boxstyle="round,pad=0.2", fc="#fcfcfb", ec="none", alpha=0.8))
ax.set_xlim(0, 40)
ax.set_ylim(0, 30)
ax.set_aspect("equal")
ax.grid(False)
ax.set_xlabel("km east")
ax.set_ylabel("km north")
ax.set_title("Card transactions per hexagon (each hex ≈ 0.8 km², simulated)")
cb = fig.colorbar(hb, ax=ax, shrink=0.8, pad=0.02)
cb.set_label("Transactions per hex (log scale)")
cb.outline.set_visible(False)
fig.tight_layout()
