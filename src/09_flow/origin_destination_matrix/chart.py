# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import seaborn as sns

# %% data
rng = np.random.default_rng(8)
districts = ["Central", "North", "East", "South", "West", "Harbor", "Hills", "Airport"]
attract = np.array([10, 3, 4, 3, 3, 5, 1, 4])        # job centers
pop = np.array([4, 8, 6, 9, 7, 3, 5, 2])
flows = np.outer(pop, attract) * rng.uniform(0.6, 1.4, (8, 8))
np.fill_diagonal(flows, 0)
od = pd.DataFrame(flows.round(0), index=districts, columns=districts)
od.iloc[:4, :4]

# %% plot
fig, ax = plt.subplots(figsize=(8, 6.5))
mask = np.eye(len(od), dtype=bool)
sns.heatmap(od, mask=mask, cmap=SEQ_CMAP, annot=True, fmt=".0f", linewidths=2,
            linecolor="#fcfcfb", cbar_kws=dict(label="commuters (thousands/day)"),
            annot_kws=dict(fontsize=8.5), ax=ax)
ax.set_xlabel("Destination (work)")
ax.set_ylabel("Origin (home)")
ax.set_title("Daily commuter flows between districts")
ax.tick_params(axis="x", rotation=30)
ax.grid(False)
fig.tight_layout()
