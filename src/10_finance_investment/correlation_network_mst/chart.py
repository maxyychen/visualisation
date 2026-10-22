# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import networkx as nx

# %% data
rng = np.random.default_rng(21)
sectors = {"Tech": 7, "Financials": 6, "Energy": 5, "Healthcare": 6}
tickers, sector_of = [], {}
for s, k in sectors.items():
    for i in range(k):
        t = f"{s[:3].upper()}{i + 1}"
        tickers.append(t)
        sector_of[t] = s
n_days = 504
market = rng.normal(0.0004, 0.010, n_days)
sector_f = {s: rng.normal(0, 0.008, n_days) for s in sectors}
rets = pd.DataFrame({
    t: rng.uniform(0.6, 1.3) * market + rng.uniform(0.6, 1.2) * sector_f[sector_of[t]]
       + rng.normal(0, 0.009, n_days)
    for t in tickers})
corr = rets.corr()
corr.round(2).iloc[:5, :5]

# %% plot
dist = np.sqrt(2 * (1 - corr))
G = nx.Graph()
for i, a in enumerate(tickers):
    for b in tickers[i + 1:]:
        G.add_edge(a, b, weight=dist.loc[a, b], corr=corr.loc[a, b])
mst = nx.minimum_spanning_tree(G, weight="weight")
pos = nx.kamada_kawai_layout(mst, weight="weight")

fig, ax = plt.subplots(figsize=(9, 7))
for a, b, d in mst.edges(data=True):
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.plot([x1, x2], [y1, y2], color="#b8b7b1", linewidth=0.5 + 5 * max(d["corr"] - 0.2, 0), zorder=1)
for k, s in enumerate(sectors):
    nodes = [t for t in mst.nodes if sector_of[t] == s]
    xy = np.array([pos[t] for t in nodes])
    deg = np.array([mst.degree(t) for t in nodes])
    ax.scatter(xy[:, 0], xy[:, 1], s=120 + 90 * deg, color=PALETTE[k], edgecolor="#fcfcfb",
               linewidth=2, zorder=3, label=s)
for t, (x, y) in pos.items():
    ax.annotate(t, (x, y), xytext=(0, 11), textcoords="offset points", ha="center", fontsize=8,
                color="#52514e", zorder=4)
ax.set_axis_off()
ax.set_title("Minimum spanning tree of stock correlations: sectors form branches")
ax.legend(loc="lower left", title="Sector", fontsize=9, title_fontsize=9)
fig.text(0.01, 0.01, "Distance d = √(2(1−ρ)) on 2 years of daily returns · node size = number of links · "
         "line width = correlation", fontsize=8, color="#7a7974")
fig.tight_layout()
