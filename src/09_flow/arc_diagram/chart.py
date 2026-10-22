# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.patches import Arc

# %% data
chapters = [f"Co {c}" for c in "ABCDEFGHIJKL"]
refs = pd.DataFrame([(1, 3, 2), (1, 5, 1), (2, 3, 3), (2, 8, 1), (3, 4, 4), (3, 9, 2),
                     (4, 6, 2), (5, 6, 3), (5, 11, 1), (6, 7, 2), (7, 10, 3), (8, 9, 2),
                     (9, 12, 1), (10, 11, 2), (1, 12, 1), (4, 10, 1)],
                    columns=["from", "to", "refs"])  # refs = shared directors
refs.head()

# %% plot
fig, ax = plt.subplots(figsize=(10, 4.8))
for f, t, w in refs.itertuples(index=False):
    center, width = (f + t) / 2, abs(t - f)
    ax.add_patch(Arc((center, 0), width, width, theta1=0, theta2=180,
                     color=PALETTE[0], linewidth=0.8 + 1.0 * w, alpha=0.6))
strength = refs.groupby("from")["refs"].sum().add(refs.groupby("to")["refs"].sum(), fill_value=0)
xs = np.arange(1, 13)
ax.scatter(xs, np.zeros(12), s=[40 + 25 * strength.get(i, 0) for i in xs], color=PALETTE[1],
           zorder=3, edgecolor="#fcfcfb", linewidth=1.5)
for x, c in zip(xs, chapters):
    ax.text(x, -0.35, c, ha="center", va="top", fontsize=9)
ax.set_xlim(0.3, 12.7)
ax.set_ylim(-1, 6.2)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Board interlocks among 12 listed companies (arc width = shared directors)")
fig.tight_layout()
