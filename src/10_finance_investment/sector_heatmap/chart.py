# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import squarify
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

# %% data
rng = np.random.default_rng(8)
sectors = {
    "Technology": ["AAPX", "MSFX", "NVDX", "AVGX", "ORCX", "CRMX", "ADBX"],
    "Financials": ["JPMX", "BACX", "WFCX", "GSX", "MSX"],
    "Health care": ["LLYX", "UNHX", "JNJX", "MRKX", "ABBX"],
    "Consumer": ["AMZX", "TSLX", "HDX", "MCDX", "NKEX"],
    "Energy": ["XOMX", "CVXX", "COPX"],
    "Industrials": ["CATX", "GEX", "HONX", "UPSX", "DEX", "LMX"],
}
sector_move = {"Technology": 1.5, "Financials": -0.5, "Health care": 0.3,
               "Consumer": -1.0, "Energy": -2.1, "Industrials": 0.4}
rows = []
for sector, tickers in sectors.items():
    for t in tickers:
        rows.append({"sector": sector, "ticker": t,
                     "mcap_bn": rng.lognormal(5.2, 0.8),
                     "ret_pct": sector_move[sector] + rng.normal(0, 0.8)})
df = pd.DataFrame(rows).round({"mcap_bn": 0, "ret_pct": 2})
df.sort_values("mcap_bn", ascending=False).head()

# %% plot
cmap = LinearSegmentedColormap.from_list("loss_gain", [PALETTE[1], "#e3e2de", PALETTE[0]])
norm = TwoSlopeNorm(vmin=-3, vcenter=0, vmax=3)
W, H, header = 100, 60, 3.4

fig, ax = plt.subplots(figsize=(11, 6.6))
by_sector = df.groupby("sector")["mcap_bn"].sum().sort_values(ascending=False)
sector_rects = squarify.squarify(squarify.normalize_sizes(by_sector.values, W, H), 0, 0, W, H)
for sector, r in zip(by_sector.index, sector_rects):
    ax.add_patch(plt.Rectangle((r["x"], r["y"]), r["dx"], r["dy"], facecolor="#efeee9", linewidth=0))
    sub = df[df["sector"] == sector].sort_values("mcap_bn", ascending=False)
    inner_h = r["dy"] - header
    tiles = squarify.squarify(squarify.normalize_sizes(sub["mcap_bn"].values, r["dx"], inner_h),
                              r["x"], r["y"], r["dx"], inner_h)
    for (_, row), q in zip(sub.iterrows(), tiles):
        ax.add_patch(plt.Rectangle((q["x"], q["y"]), q["dx"], q["dy"],
                                   facecolor=cmap(norm(np.clip(row["ret_pct"], -3, 3))),
                                   edgecolor="#fcfcfb", linewidth=1.5))
        if q["dx"] > 6 and q["dy"] > 4.5:
            ink = "white" if abs(row["ret_pct"]) >= 2 else "#0b0b0b"
            ax.text(q["x"] + q["dx"] / 2, q["y"] + q["dy"] / 2,
                    f"{row['ticker']}\n{row['ret_pct']:+.1f}%", ha="center", va="center",
                    fontsize=8.5, color=ink)
    ax.add_patch(plt.Rectangle((r["x"], r["y"]), r["dx"], r["dy"], fill=False,
                               edgecolor="#fcfcfb", linewidth=4))
    ax.text(r["x"] + 0.8, r["y"] + r["dy"] - 0.5, sector.upper(), ha="left", va="top",
            fontsize=8, fontweight="bold", color="#52514e")

ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
cb = fig.colorbar(sm, ax=ax, fraction=0.025, pad=0.01, ticks=[-3, -2, -1, 0, 1, 2, 3])
cb.set_label("Daily return (%), clipped at ±3")
cb.outline.set_visible(False)
ax.set_title("Market map: tile size = market cap, color = today's return (fictional tickers)")
fig.tight_layout()
