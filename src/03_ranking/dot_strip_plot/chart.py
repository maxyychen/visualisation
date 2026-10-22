# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(2)
metrics = ["Safety", "Healthcare", "Education", "Housing cost", "Transit"]
cities = [f"City {i}" for i in range(29)] + ["Our city"]
rows = [(c, m, rng.uniform(30, 95)) for c in cities for m in metrics]
df = pd.DataFrame(rows, columns=["city", "metric", "score"])
ours = {"Safety": 88, "Healthcare": 74, "Education": 52, "Housing cost": 35, "Transit": 81}
df.loc[df["city"] == "Our city", "score"] = df.loc[df["city"] == "Our city", "metric"].map(ours)
df["rank"] = df.groupby("metric")["score"].rank(ascending=False).astype(int)
df[df["city"] == "Our city"]

# %% plot
fig, ax = plt.subplots(figsize=(8.5, 4.5))
for y, m in enumerate(metrics):
    g = df[df["metric"] == m]
    others = g[g["city"] != "Our city"]
    ax.scatter(others["score"], np.full(len(others), y), s=70, color=GRAY, alpha=0.6,
               edgecolor="#fcfcfb", linewidth=1)
    me = g[g["city"] == "Our city"].iloc[0]
    ax.scatter(me["score"], y, s=110, color=PALETTE[0], zorder=3, edgecolor="#fcfcfb", linewidth=1.5)
    ax.annotate(f"#{me['rank']}", (me["score"], y), xytext=(0, 10), textcoords="offset points",
                ha="center", fontsize=9, color="#0b0b0b", weight="bold")
ax.set_yticks(range(len(metrics)), metrics)
ax.set_ylim(-0.6, len(metrics) - 0.3)
ax.invert_yaxis()
ax.set_xlabel("Score (0–100)")
ax.set_title("Where our city ranks among 30 cities")
ax.grid(axis="y", visible=False)
fig.tight_layout()
