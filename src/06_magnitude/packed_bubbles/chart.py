# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(17)
df = pd.DataFrame({"company": [f"Co. {c}" for c in "ABCDEFGHIJKLMNO"],
                   "market_cap_bn": np.sort(rng.lognormal(4.5, 0.9, 15))[::-1].round()})
df["sector"] = ["Tech", "Tech", "Finance", "Health", "Tech", "Energy", "Finance", "Health",
                "Energy", "Tech", "Finance", "Health", "Energy", "Tech", "Finance"]
df.head()

# %% plot
# simple greedy circle packing: place each circle as close to the center as possible
radii = np.sqrt(df["market_cap_bn"].values / np.pi)
placed = []
for r in radii:
    if not placed:
        placed.append((0.0, 0.0, r)); continue
    best = None
    for ang in np.linspace(0, 2 * np.pi, 180, endpoint=False):
        for dist in np.linspace(0, 60, 400):
            x, y = dist * np.cos(ang), dist * np.sin(ang)
            if all(np.hypot(x - px, y - py) >= r + pr + 0.3 for px, py, pr in placed):
                if best is None or dist < best[0]:
                    best = (dist, x, y)
                break
    placed.append((best[1], best[2], r))
sectors = list(dict.fromkeys(df["sector"]))
fig, ax = plt.subplots(figsize=(7, 7))
for (x, y, r), (_, row) in zip(placed, df.iterrows()):
    c = PALETTE[sectors.index(row["sector"])]
    ax.add_patch(plt.Circle((x, y), r, color=c, alpha=0.85, ec="#fcfcfb", lw=2))
    if r > 4:
        ax.text(x, y, f"{row['company']}\n${row['market_cap_bn']:.0f}B", ha="center",
                va="center", fontsize=8.5, color="white", fontweight="bold")
lim = max(abs(v) + r for x, y, r in placed for v in (x, y)) + 1
ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
ax.set_aspect("equal"); ax.axis("off")
for i, s in enumerate(sectors):
    ax.scatter([], [], color=PALETTE[i], s=80, label=s)
ax.legend(loc="upper left", bbox_to_anchor=(0, 1.0), ncol=4)
ax.set_title("Market capitalisation by company")
fig.tight_layout()
