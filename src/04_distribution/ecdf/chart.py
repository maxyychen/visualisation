# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(29)
df = pd.concat([
    pd.DataFrame({"version": "v1", "latency_ms": rng.lognormal(5.6, 0.45, 3000)}),
    pd.DataFrame({"version": "v2", "latency_ms": rng.lognormal(5.35, 0.35, 3000)}),
], ignore_index=True)
df.groupby("version")["latency_ms"].quantile([0.5, 0.95]).unstack().round(0)

# %% plot
import seaborn as sns
fig, ax = plt.subplots(figsize=(8, 4.8))
sns.ecdfplot(data=df, x="latency_ms", hue="version", palette=PALETTE[:2], linewidth=2, ax=ax)
for q in [0.5, 0.95]:
    ax.axhline(q, color="#52514e", linewidth=0.8)
    ax.text(1450, q + 0.015, f"p{int(q * 100)}", fontsize=9, color="#52514e", ha="right")
ax.set_xlim(0, 1500)
ax.set_xlabel("Page-load latency (ms)")
ax.set_ylabel("Share of requests ≤ x")
ax.set_title("Latency distribution: v2 is faster across the board")
ax.get_legend().set_title(None)
fig.tight_layout()

# %% alt:plotly
import plotly.express as px
fig = px.ecdf(df, x="latency_ms", color="version", color_discrete_sequence=PALETTE,
              labels={"latency_ms": "Page-load latency (ms)", "version": ""},
              title="Latency distribution: v2 is faster across the board")
for q in [0.5, 0.95]:
    fig.add_hline(y=q, line_color="#52514e", line_width=0.8, annotation_text=f"p{int(q * 100)}")
fig.update_layout(xaxis_range=[0, 1500], yaxis_title="Share of requests ≤ x")
fig.show()
