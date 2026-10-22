# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(7)
products = [f"Product {c}" for c in "ABCDEFGHIJKL"]
df = pd.DataFrame({"product": products,
                   "yoy_change_pct": rng.normal(2, 9, len(products)).round(1)})
df = df.sort_values("yoy_change_pct")
df.head()

# %% plot
colors = np.where(df["yoy_change_pct"] >= 0, PALETTE[0], PALETTE[1])
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.barh(df["product"], df["yoy_change_pct"], color=colors, height=0.7)
ax.axvline(0, color="#52514e", linewidth=1)
for y, v in enumerate(df["yoy_change_pct"]):
    ax.text(v + (0.4 if v >= 0 else -0.4), y, f"{v:+.1f}%", va="center",
            ha="left" if v >= 0 else "right", fontsize=9, color="#52514e")
ax.set_xlabel("Change vs. last year (%)")
ax.set_title("Year-over-year sales change by product")
ax.grid(axis="y", visible=False)
lim = df["yoy_change_pct"].abs().max() * 1.25
ax.set_xlim(-lim, lim)
fig.tight_layout()
