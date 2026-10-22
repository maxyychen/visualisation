# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame({"clinic": ["Clinic A", "Clinic B", "Clinic C", "Clinic D"],
                   "patients_k": [1, 2, 4, 8]})
df

# %% plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
xs = np.array([0.5, 1.6, 3.0, 5.0])
for ax, mode in [(ax1, "radius"), (ax2, "area")]:
    v = df["patients_k"].to_numpy()
    radius = 0.11 * v if mode == "radius" else 0.31 * np.sqrt(v)   # data units
    for x, r, name, val in zip(xs, radius, df["clinic"], v):
        ax.add_patch(plt.Circle((x, r), r, color=PALETTE[0] if mode == "area" else PALETTE[7],
                                alpha=0.85, linewidth=0))
        ax.text(x, -0.25, f"{name}\n{val}k", ha="center", va="top", fontsize=9.5, color="#52514e")
    ax.set_xlim(-0.3, 6.1)
    ax.set_ylim(-0.75, 2.0)
    ax.set_aspect("equal")
    ax.axis("off")
ax1.set_title("✗ Misleading: radius ∝ value (8× looks like 64×)", fontsize=11.5)
ax2.set_title("✓ Better: area ∝ value (8× looks like 8×)", fontsize=11.5)
fig.tight_layout()
