# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
partners = ["China", "USA", "Japan", "Germany", "Korea", "Vietnam", "India", "Brazil"]
exports = np.array([120, 95, 40, 28, 25, 18, 12, 8])
imports = np.array([140, 70, 52, 30, 33, 10, 15, 11])
df = pd.DataFrame({"partner": partners, "exports": exports, "imports": imports})
df = df.iloc[::-1]
df

# %% plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(df["partner"], -df["imports"], color=PALETTE[1], label="Imports", height=0.7)
ax.barh(df["partner"], df["exports"], color=PALETTE[0], label="Exports", height=0.7)
ax.axvline(0, color="#52514e", linewidth=1)
ticks = np.arange(-150, 151, 50)
ax.set_xticks(ticks, [f"{abs(t)}" for t in ticks])
ax.set_xlabel("USD bn   (← imports | exports →)")
ax.set_title("Trade by partner")
ax.grid(axis="y", visible=False)
ax.legend(loc="lower right")
fig.tight_layout()
