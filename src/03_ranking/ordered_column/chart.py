# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
teams = ["USA", "CHN", "JPN", "GBR", "AUS", "FRA", "NED", "KOR", "ITA", "GER"]
medals = [113, 91, 58, 65, 46, 64, 34, 32, 40, 33]
df = pd.DataFrame({"team": teams, "medals": medals}).sort_values("medals", ascending=False)
df

# %% plot
fig, ax = plt.subplots(figsize=(8.5, 4.5))
ax.bar(df["team"], df["medals"], color=PALETTE[0], width=0.7)
for x, v in enumerate(df["medals"]):
    ax.text(x, v + 1.5, str(v), ha="center", fontsize=9, color="#52514e")
ax.set_ylabel("Total medals")
ax.set_title("Medal table: top 10 teams")
ax.grid(axis="x", visible=False)
fig.tight_layout()
