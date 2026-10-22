# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
seasons = ["18/19", "19/20", "20/21", "21/22", "22/23", "23/24"]
ranks = {
    "Rovers":   [1, 1, 2, 3, 5, 6],
    "United":   [5, 4, 3, 1, 1, 2],
    "City":     [2, 2, 1, 2, 3, 1],
    "Athletic": [8, 7, 6, 5, 2, 3],
    "Wanderers":[3, 3, 4, 4, 4, 4],
    "Albion":   [4, 5, 5, 7, 6, 5],
    "Town":     [6, 8, 8, 6, 7, 8],
    "Rangers":  [7, 6, 7, 8, 8, 7],
}
df = pd.DataFrame(ranks, index=seasons)
df

# %% plot
fig, ax = plt.subplots(figsize=(8.5, 5))
highlight = {"Rovers": PALETTE[1], "Athletic": PALETTE[2], "City": PALETTE[0]}
x = np.arange(len(df))
for team in df.columns:
    color = highlight.get(team, GRAY)
    z, lw = (3, 2.5) if team in highlight else (1, 1.5)
    ax.plot(x, df[team], color=color, linewidth=lw, marker="o", markersize=9,
            markeredgecolor="#fcfcfb", markeredgewidth=1.5, zorder=z)
    ax.text(x[-1] + 0.15, df[team].iloc[-1], team, va="center", fontsize=9.5,
            color="#0b0b0b" if team in highlight else "#52514e",
            weight="bold" if team in highlight else "normal")
ax.set_yticks(range(1, 9))
ax.invert_yaxis()
ax.set_xticks(x, df.index)
ax.set_xlim(-0.3, len(df) - 0.1)
ax.set_ylabel("League position")
ax.set_title("League standings by season")
ax.grid(axis="x", visible=False)
fig.tight_layout()
