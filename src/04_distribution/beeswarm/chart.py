# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(23)
levels = {"Junior": 70, "Mid": 95, "Senior": 125, "Lead": 150}
rows = []
for lvl, mu in levels.items():
    n = 62
    rows.append(pd.DataFrame({"level": lvl,
                              "salary_k": rng.normal(mu, mu * 0.13, n),
                              "work": rng.choice(["Remote", "On-site"], n, p=[0.45, 0.55])}))
df = pd.concat(rows, ignore_index=True)
df.groupby("level", sort=False)["salary_k"].median().round(0)

# %% plot
import seaborn as sns
fig, ax = plt.subplots(figsize=(8.5, 5.5))
sns.swarmplot(data=df, x="level", y="salary_k", hue="work", palette=PALETTE[:2],
              size=5, edgecolor="#fcfcfb", linewidth=0.4, ax=ax)
ax.set_xlabel(None)
ax.set_ylabel("Salary ($k)")
ax.set_title("Data scientist salaries by seniority")
ax.legend(title=None, loc="upper left")
ax.grid(axis="x", visible=False)
fig.tight_layout()
