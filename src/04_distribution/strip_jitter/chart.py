# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(19)
arms = {"No promotion": (1, 4), "10% discount": (7, 5), "Buy 2 get 1": (11, 6)}
df = pd.concat([pd.DataFrame({"arm": a, "uplift_pct": rng.normal(m, s, 40)})
                for a, (m, s) in arms.items()], ignore_index=True)
df.groupby("arm")["uplift_pct"].agg(["mean", "std", "count"]).round(1)

# %% plot
import seaborn as sns
fig, ax = plt.subplots(figsize=(7, 5))
sns.stripplot(data=df, x="arm", y="uplift_pct", hue="arm", palette=PALETTE[:3], legend=False,
              jitter=0.22, size=6, alpha=0.75, edgecolor="#fcfcfb", linewidth=0.6, ax=ax)
means = df.groupby("arm", sort=False)["uplift_pct"].mean()
for i, m in enumerate(means):
    ax.hlines(m, i - 0.32, i + 0.32, color="#0b0b0b", linewidth=2.2, zorder=4)
    ax.text(i + 0.36, m, f"{m:.0f}%", va="center", fontsize=9)
ax.axhline(0, color="#52514e", linewidth=0.8)
ax.set_xlabel(None)
ax.set_ylabel("Sales uplift vs. last year (%)")
ax.set_title("Sales uplift by promotion (n = 40 stores each)")
ax.grid(axis="x", visible=False)
fig.tight_layout()
