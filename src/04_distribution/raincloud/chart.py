# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(37)
conds = {"No caffeine": (420, 60), "1 cup": (385, 50), "3 cups": (395, 75)}
df = pd.concat([pd.DataFrame({"condition": c, "rt_ms": rng.normal(m, s, 80)})
                for c, (m, s) in conds.items()], ignore_index=True)
df.groupby("condition", sort=False)["rt_ms"].describe().round(0)

# %% plot
fig, ax = plt.subplots(figsize=(8.5, 5))
groups = list(conds)
rng_j = np.random.default_rng(0)
for i, (g, color) in enumerate(zip(groups, PALETTE)):
    vals = df.loc[df["condition"] == g, "rt_ms"].values
    v = ax.violinplot(vals, positions=[i], vert=False, widths=0.9,
                      showextrema=False)
    body = v["bodies"][0]
    verts = body.get_paths()[0].vertices
    verts[:, 1] = np.clip(verts[:, 1], i, None)       # keep the upper half: the "cloud"
    body.set_facecolor(color); body.set_alpha(0.45); body.set_edgecolor("none")
    ax.boxplot(vals, positions=[i - 0.08], vert=False, widths=0.07, patch_artist=True,
               showfliers=False, boxprops=dict(facecolor="#fcfcfb", edgecolor="#0b0b0b"),
               medianprops=dict(color="#0b0b0b", linewidth=1.8),
               whiskerprops=dict(color="#0b0b0b"), capprops=dict(color="#0b0b0b"))
    ax.scatter(vals, i - 0.25 + rng_j.uniform(-0.07, 0.07, len(vals)), s=10,
               color=color, alpha=0.7, edgecolor="none")
ax.set_yticks(range(len(groups)), groups)
ax.set_ylim(-0.5, len(groups) - 0.3)
ax.set_xlabel("Reaction time (ms)")
ax.set_title("Reaction time by caffeine dose")
ax.grid(axis="y", visible=False)
fig.tight_layout()
