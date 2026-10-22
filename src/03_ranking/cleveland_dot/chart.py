# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
countries = ["Japan", "Spain", "Korea", "Italy", "France", "Canada", "UK", "Germany",
             "Chile", "USA", "China", "Brazil"]
women = [87.6, 86.2, 86.5, 85.6, 85.7, 84.5, 83.0, 83.4, 82.5, 80.2, 80.5, 79.4]
men = [81.6, 80.9, 80.3, 81.2, 79.7, 80.5, 79.4, 78.6, 77.3, 74.8, 75.2, 72.8]
df = pd.DataFrame({"country": countries, "women": women, "men": men})
df = df.sort_values("women").reset_index(drop=True)
df.tail()

# %% plot
fig, ax = plt.subplots(figsize=(7.5, 5.5))
ax.hlines(df.index, df["men"], df["women"], color="#d0cfca", linewidth=1.5, zorder=1)
ax.scatter(df["women"], df.index, s=60, color=PALETTE[0], label="Women", zorder=3,
           edgecolor="#fcfcfb", linewidth=1.5)
ax.scatter(df["men"], df.index, s=60, color=PALETTE[1], label="Men", zorder=3,
           edgecolor="#fcfcfb", linewidth=1.5)
ax.set_yticks(df.index, df["country"])
ax.set_xlabel("Life expectancy at birth (years)")
ax.set_title("Life expectancy by country and sex")
ax.legend(loc="lower right")
ax.grid(axis="y", color="#efeeeb")
fig.tight_layout()
