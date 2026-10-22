# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame({"ward": ["Ward A", "Ward B", "Ward C", "Ward D"],
                   "score": [92.0, 93.5, 95.0, 97.0]})
df

# %% plot
fig = plt.figure(figsize=(12, 5))
gs = fig.add_gridspec(2, 2, height_ratios=[3, 1.3], width_ratios=[1, 1])
ax1 = fig.add_subplot(gs[:, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 1])

# Misleading: bars on an axis that starts at 91.
ax1.bar(df["ward"], df["score"], color=PALETTE[0], width=0.6)
ax1.set_ylim(91, 97.5)
ax1.set_ylabel("Satisfaction score")
ax1.set_title("✗ Misleading: bars on a truncated axis (starts at 91)", fontsize=11.5)
ax1.grid(axis="x", visible=False)

# Better: bars from zero, values labeled ...
ax2.bar(df["ward"], df["score"], color=PALETTE[0], width=0.6)
for x, v in enumerate(df["score"]):
    ax2.text(x, v + 2, f"{v:.1f}", ha="center", fontsize=9.5, color="#52514e")
ax2.set_ylim(0, 110)
ax2.set_yticks([0, 25, 50, 75, 100])
ax2.set_ylabel("Score")
ax2.set_title("✓ Better: bars start at zero …", fontsize=11.5)
ax2.grid(axis="x", visible=False)

# ... or a dot plot, which may zoom because it encodes position.
ax3.hlines(0, 90, 100, color="#e6e5e1", linewidth=1)
ax3.scatter(df["score"], np.zeros(len(df)), s=70, color=PALETTE[0], zorder=3,
            edgecolor="#fcfcfb", linewidth=1.5)
for v, w in zip(df["score"], df["ward"]):
    ax3.text(v, 0.5, w.replace("Ward ", ""), ha="center", fontsize=9, color="#52514e")
ax3.set_xlim(90, 100)
ax3.set_ylim(-0.6, 1.0)
ax3.set_yticks([])
ax3.spines["left"].set_visible(False)
ax3.grid(axis="y", visible=False)
ax3.set_xlabel("… or a dot plot (zooming is fine: position, not length)")
fig.tight_layout()
