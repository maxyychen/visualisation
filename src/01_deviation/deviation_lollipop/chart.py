# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(11)
models = [f"Model {i:02d}" for i in range(1, 21)]
mpg = rng.normal(28, 6, len(models)).round(1)
df = pd.DataFrame({"model": models, "mpg": mpg})
df["dev"] = df["mpg"] - df["mpg"].mean()
df = df.sort_values("dev").reset_index(drop=True)
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(8, 6.5))
colors = np.where(df["dev"] >= 0, PALETTE[0], PALETTE[1])
ax.hlines(df.index, 0, df["dev"], color=colors, linewidth=1.5)
ax.scatter(df["dev"], df.index, color=colors, s=60, zorder=3,
           edgecolor="#fcfcfb", linewidth=1.5)
ax.axvline(0, color="#52514e", linewidth=1)
ax.set_yticks(df.index, df["model"])
ax.set_xlabel(f"Difference from fleet average ({df['mpg'].mean():.1f} mpg)")
ax.set_title("Fuel efficiency relative to fleet average")
ax.grid(axis="y", visible=False)
fig.tight_layout()
