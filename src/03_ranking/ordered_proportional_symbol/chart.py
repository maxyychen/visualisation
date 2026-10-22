# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
cities = ["Tokyo", "Delhi", "Shanghai", "Dhaka", "São Paulo", "Cairo", "Mexico City",
          "Beijing", "Mumbai", "Osaka"]
pop = [37.1, 33.8, 29.9, 23.9, 22.8, 22.6, 22.5, 22.2, 21.7, 19.0]
df = pd.DataFrame({"city": cities, "pop_m": pop}).sort_values("pop_m", ascending=False)
df

# %% plot
fig, ax = plt.subplots(figsize=(10, 3.4))
r = np.sqrt(df["pop_m"].values / np.pi)            # area proportional to value
r = r / r.max() * 0.45
x = np.cumsum(np.r_[r[0], r[:-1] + r[1:] + 0.06])
for xi, ri, (_, row) in zip(x, r, df.iterrows()):
    ax.add_patch(plt.Circle((xi, 0), ri, color=PALETTE[0], alpha=0.85))
    ax.text(xi, 0, f"{row['pop_m']:.0f}", ha="center", va="center", color="white",
            fontsize=10, weight="bold")
    ax.text(xi, -0.55, row["city"], ha="center", va="top", fontsize=9, color="#52514e")
ax.set_xlim(-0.05, x[-1] + r[-1] + 0.05)
ax.set_ylim(-0.8, 0.5)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Largest metropolitan areas (population, millions)")
fig.tight_layout()
