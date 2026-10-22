# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import squarify

# %% data
df = pd.DataFrame({
    "division": ["Technology"] * 5 + ["Financials"] * 3 + ["Healthcare"] * 3 + ["Energy"] * 2,
    "holding": ["Software Co", "Chipmaker", "Cloud Co", "Hardware Co", "Payments Co",
             "Big Bank", "Insurer", "Asset Mgr",
             "Pharma Co", "MedTech Co", "Biotech Co",
             "Oil Major", "Utility Co"],
    "value_m": [58, 44, 30, 26, 14, 22, 12, 6, 18, 15, 11, 7, 5],
}).sort_values(["division", "value_m"], ascending=[True, False])
df

# %% plot
divisions = ["Technology", "Financials", "Healthcare", "Energy"]
cmap = dict(zip(divisions, PALETTE))
df = df.sort_values("value_m", ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
labels = [f"{d}\n${v}M" if v >= 10 else "" for d, v in zip(df["holding"], df["value_m"])]
squarify.plot(sizes=df["value_m"], label=labels, color=[cmap[d] for d in df["division"]],
              ax=ax, pad=False, edgecolor="#fcfcfb", linewidth=2,
              text_kwargs=dict(color="white", fontsize=9.5, fontweight="bold"))
ax.axis("off")
handles = [plt.Rectangle((0, 0), 1, 1, color=cmap[d]) for d in divisions]
ax.legend(handles, divisions, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.01))
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
