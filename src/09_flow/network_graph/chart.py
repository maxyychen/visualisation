# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import networkx as nx

# %% data
G = nx.planted_partition_graph(3, 13, p_in=0.35, p_out=0.02, seed=4)
group = {n: n // 13 for n in G.nodes}
# one bridge author connected to all groups
G.add_node(39)
group[39] = 3
G.add_edges_from([(39, 0), (39, 14), (39, 27), (39, 5)])
G.remove_nodes_from(list(nx.isolates(G)))
print(G)

# %% plot
pos = nx.spring_layout(G, seed=7, k=0.35)
deg = dict(G.degree())
group_names = ["Genomics", "Imaging", "Epidemiology", "Bridge"]
fig, ax = plt.subplots(figsize=(8, 7))
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#c9c8c3", width=0.8)
for g in range(4):
    ns = [n for n in G.nodes if group[n] == g]
    nx.draw_networkx_nodes(G, pos, nodelist=ns, ax=ax, node_color=PALETTE[g],
                           node_size=[40 + 30 * deg[n] for n in ns],
                           edgecolors="#fcfcfb", linewidths=1.5, label=group_names[g])
ax.annotate("bridge author", pos[39], xytext=(15, 15), textcoords="offset points",
            fontsize=9, arrowprops=dict(arrowstyle="-", color="#52514e"))
ax.legend(loc="lower left", markerscale=0.6)
ax.set_title("Co-authorship network (node size = number of co-authors)")
ax.axis("off")
fig.tight_layout()
