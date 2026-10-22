# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
langs = ["JavaScript", "Python", "SQL", "TypeScript", "Java", "C#", "C++", "Go",
         "Rust", "PHP", "Kotlin", "Swift"]
share = [62.3, 51.0, 48.7, 38.5, 30.1, 27.0, 22.4, 14.2, 13.1, 12.0, 9.4, 5.1]
df = pd.DataFrame({"language": langs, "share_pct": share}).sort_values("share_pct")
df.tail()

# %% plot
fig, ax = plt.subplots(figsize=(7.5, 5.5))
colors = [PALETTE[0] if l == "Python" else GRAY for l in df["language"]]
ax.barh(df["language"], df["share_pct"], color=colors, height=0.72)
for y, v in enumerate(df["share_pct"]):
    ax.text(v + 0.8, y, f"{v:.0f}%", va="center", fontsize=9, color="#52514e")
ax.set_xlim(0, 70)
ax.xaxis.set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.grid(False)
ax.set_title("Languages used by developers (% of respondents)")
fig.tight_layout()
