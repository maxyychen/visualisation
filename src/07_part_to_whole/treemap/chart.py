# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import squarify

# %% data
df = pd.DataFrame({
    "division": ["Technology"] * 5 + ["Financials"] * 3 + ["Healthcare"] * 3 + ["Energy"] * 2,
    "holding": ["Software Co", "Chipmaker", "Cloud Co", "Hardware Co", "Payments Co",
             "Big Bank", "Insurer", "Asset Mgr",
             "Pharma Co", "MedTech Co", "Biotech Co",
             "Oil Major", "Pipeline Co"],
    "value_m": [58, 44, 30, 26, 14, 22, 12, 6, 18, 15, 11, 7, 5],
}).sort_values(["division", "value_m"], ascending=[True, False])
df

# %% plot
divisions = ["Technology", "Financials", "Healthcare", "Energy"]
cmap = dict(zip(divisions, PALETTE))
W, H = 100, 60
totals = df.groupby("division")["value_m"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
# level 1: one rectangle per sector; level 2: holdings squarified inside their sector
sector_rects = squarify.squarify(squarify.normalize_sizes(totals.values, W, H), 0, 0, W, H)
for div, sr in zip(totals.index, sector_rects):
    g = df[df["division"] == div].sort_values("value_m", ascending=False)
    rects = squarify.squarify(squarify.normalize_sizes(g["value_m"].values, sr["dx"], sr["dy"]),
                              sr["x"], sr["y"], sr["dx"], sr["dy"])
    for (_, row), r in zip(g.iterrows(), rects):
        ax.add_patch(plt.Rectangle((r["x"], r["y"]), r["dx"], r["dy"], facecolor=cmap[div],
                                   edgecolor="#fcfcfb", linewidth=1.5))
        if row["value_m"] >= 10:
            ax.text(r["x"] + r["dx"] / 2, r["y"] + r["dy"] / 2, f"{row['holding']}\n${row['value_m']}M",
                    ha="center", va="center", color="white", fontsize=9.5, fontweight="bold")
    ax.add_patch(plt.Rectangle((sr["x"], sr["y"]), sr["dx"], sr["dy"], fill=False,
                               edgecolor="#fcfcfb", linewidth=5))   # thick gap between sectors
ax.set_xlim(0, W); ax.set_ylim(0, H)
ax.axis("off")
handles = [plt.Rectangle((0, 0), 1, 1, color=cmap[d]) for d in divisions]
ax.legend(handles, [f"{d} (${totals[d]}M)" for d in divisions], ncol=4, loc="upper center",
          bbox_to_anchor=(0.5, -0.01))
ax.set_title(f"Equity portfolio by sector and holding (total ${df['value_m'].sum()}M)")
fig.tight_layout()

# %% alt:plotly
import plotly.express as px
fig = px.treemap(df, path=[px.Constant("Portfolio"), "division", "holding"], values="value_m",
                 color="division", color_discrete_sequence=PALETTE,
                 title=f"Equity portfolio by sector and holding (total ${df['value_m'].sum()}M)")
fig.update_traces(root_color="#eeeeea", texttemplate="%{label}<br>$%{value}M",
                  marker=dict(line=dict(color="#fcfcfb", width=2)))
fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
fig.show()   # click a division to zoom in
