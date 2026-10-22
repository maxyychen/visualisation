# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
regions = ["Asia", "Europe", "N. America", "LatAm", "Africa"]
size = pd.Series([620, 210, 170, 120, 80], index=regions)  # units, millions
share = pd.DataFrame({
    "Brand A": [22, 30, 50, 12, 10],
    "Brand B": [20, 33, 25, 28, 22],
    "Brand C": [25, 12, 8, 30, 35],
    "Other":   [33, 25, 17, 30, 33],
}, index=regions)
share.assign(total_units_m=size)

# %% plot
fig, ax = plt.subplots(figsize=(10, 5.5))
widths = size / size.sum() * 100
lefts = np.concatenate([[0], np.cumsum(widths)[:-1]])
colors = PALETTE[:3] + [GRAY]
for x, w, region in zip(lefts, widths, regions):
    bottom = 0
    for j, brand in enumerate(share.columns):
        h = share.loc[region, brand]
        ax.bar(x, h, width=w, bottom=bottom, align="edge", color=colors[j],
               edgecolor="#fcfcfb", linewidth=2, label=brand if region == regions[0] else None)
        if w > 8 and h >= 10:
            ax.text(x + w / 2, bottom + h / 2, f"{h}%", ha="center", va="center",
                    color="white", fontsize=8.5, fontweight="bold")
        bottom += h
    ax.text(x + w / 2, 102, f"{region}\n{size[region]}M", ha="center", va="bottom", fontsize=9)
ax.set_xlim(0, 100)
ax.set_ylim(0, 115)
ax.set_yticks(range(0, 101, 25), [f"{t}%" for t in range(0, 101, 25)])
ax.set_xlabel("Share of global market (column width)")
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
ax.grid(False)
ax.set_title("Smartphone market by region and brand", pad=28)
ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.13))
fig.tight_layout()
