# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(9)
shops = [f"Café {n}" for n in ["Aroma", "Bean", "Crema", "Dolce", "Espresso", "Filtro", "Grind",
                                "Hazel", "Iris", "Java", "Kona", "Latte", "Mocha", "Nero",
                                "Oat", "Pour", "Quill", "Roast", "Sip", "Tamp"]]
df = pd.DataFrame({"shop": shops, "score": rng.normal(78, 7, 20).clip(55, 97).round(1)})
df = df.sort_values("score").reset_index(drop=True)
df.tail()

# %% plot
fig, ax = plt.subplots(figsize=(7.5, 6.5))
ax.hlines(df.index, 0, df["score"], color=PALETTE[0], linewidth=1.5)
ax.scatter(df["score"], df.index, s=55, color=PALETTE[0], zorder=3,
           edgecolor="#fcfcfb", linewidth=1.5)
ax.set_yticks(df.index, df["shop"])
ax.set_xlim(0, 100)
ax.set_xlabel("Average rating (0–100)")
ax.set_title("Coffee shop ratings")
ax.grid(axis="y", visible=False)
fig.tight_layout()
