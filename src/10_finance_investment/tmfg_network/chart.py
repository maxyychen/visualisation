# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import networkx as nx

# %% data
rng = np.random.default_rng(23)
sectors = {"Tech": 10, "Financials": 9, "Energy": 8, "Consumer": 8, "Other": 5}
tickers, sector_of = [], {}
for s, k in sectors.items():
    for i in range(k):
        t = f"{s[:3].upper()}{i + 1}"
        tickers.append(t)
        sector_of[t] = s
n_days = 756                                    # three years of daily returns
market = rng.normal(0.0004, 0.010, n_days)
sector_f = {s: rng.normal(0, 0.007 if s != "Other" else 0.002, n_days) for s in sectors}
style_f = rng.normal(0, 0.006, n_days)          # a cross-sector "growth vs value" factor
rets = pd.DataFrame({
    t: rng.uniform(0.6, 1.3) * market + rng.uniform(0.6, 1.2) * sector_f[sector_of[t]]
       + (rng.uniform(0.4, 0.9) * style_f if sector_of[t] in ("Tech", "Consumer") else 0)
       + rng.normal(0, 0.009, n_days)
    for t in tickers})
corr = rets.corr()
corr.round(2).iloc[:5, :5]

# %% plot
def tmfg(W):
    """Triangulated Maximally Filtered Graph (Massara, Di Matteo & Aste 2016).

    Start from the 4 most connected nodes (a tetrahedron), then repeatedly insert the remaining
    node that adds the largest total weight into one triangular face. Result: planar, 3n-6 edges.
    """
    W = np.asarray(W, float).copy()
    np.fill_diagonal(W, 0)
    n = len(W)
    strength = (W * (W > W.mean())).sum(axis=1)
    clique = list(np.argsort(strength)[::-1][:4])
    edges = {(a, b) for i, a in enumerate(clique) for b in clique[i + 1:]}
    faces = [tuple(f) for f in [(clique[0], clique[1], clique[2]), (clique[0], clique[1], clique[3]),
                                (clique[0], clique[2], clique[3]), (clique[1], clique[2], clique[3])]]
    remaining = [v for v in range(n) if v not in clique]
    while remaining:
        F = np.array(faces)
        gains = W[np.ix_(remaining, F[:, 0])] + W[np.ix_(remaining, F[:, 1])] + W[np.ix_(remaining, F[:, 2])]
        vi, fi = np.unravel_index(np.argmax(gains), gains.shape)
        v, (a, b, c) = remaining.pop(vi), faces.pop(fi)
        edges |= {(v, a), (v, b), (v, c)}
        faces += [(v, a, b), (v, b, c), (v, a, c)]
    return edges


edges_t = tmfg(corr.values)
T = nx.Graph()
T.add_nodes_from(tickers)
T.add_edges_from((tickers[a], tickers[b], {"corr": corr.iloc[a, b]}) for a, b in edges_t)

dist = np.sqrt(2 * (1 - corr))
G = nx.Graph()
for i, a in enumerate(tickers):
    for b in tickers[i + 1:]:
        G.add_edge(a, b, weight=dist.loc[a, b], corr=corr.loc[a, b])
M = nx.minimum_spanning_tree(G, weight="weight")


def within_sector(graph):
    return np.mean([sector_of[a] == sector_of[b] for a, b in graph.edges])


fig, axes = plt.subplots(1, 2, figsize=(15, 7.4))
colors = {s: (PALETTE[k] if s != "Other" else GRAY) for k, s in enumerate(sectors)}
for ax, graph, name in ((axes[0], M, "Minimum spanning tree"), (axes[1], T, "TMFG")):
    lengths = {(a, b): dist.loc[a, b] for a, b in graph.edges}
    nx.set_edge_attributes(graph, lengths, "length")
    pos = nx.kamada_kawai_layout(graph, weight="length")
    for a, b, d in graph.edges(data=True):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.plot([x1, x2], [y1, y2], color="#b8b7b1", linewidth=0.4 + 3 * max(d["corr"] - 0.3, 0), zorder=1)
    deg = dict(graph.degree)
    for s in sectors:
        nodes = [t for t in graph.nodes if sector_of[t] == s]
        xy = np.array([pos[t] for t in nodes])
        ax.scatter(xy[:, 0], xy[:, 1], s=[40 + 22 * deg[t] for t in nodes], color=colors[s],
                   edgecolor="#fcfcfb", linewidth=1.5, zorder=3, label=s)
    hubs = sorted(deg, key=deg.get, reverse=True)[:5]
    for t in hubs:
        ax.annotate(t, pos[t], xytext=(0, 10), textcoords="offset points", ha="center", fontsize=8,
                    color="#52514e", zorder=4)
    ax.set_axis_off()
    ax.set_title(f"{name}: {graph.number_of_edges()} links for {graph.number_of_nodes()} stocks · "
                 f"{within_sector(graph):.0%} within a sector", fontsize=11.5)
axes[0].legend(loc="lower left", title="Sector", fontsize=9, title_fontsize=9)
fig.suptitle("Filtering a 40-stock correlation matrix: the TMFG keeps 3n−6 links instead of the MST's n−1 (simulated)",
             x=0.01, ha="left", fontsize=13.5, fontweight="bold")
fig.text(0.01, 0.01, "Node size = number of links (hubs labelled) · line width = correlation · "
         "the TMFG is planar and made of triangles and 4-cliques, so it also keeps cross-sector structure "
         "such as the Tech–Consumer style factor.", fontsize=8.5, color="#7a7974")
fig.tight_layout(rect=(0, 0.03, 1, 1))
