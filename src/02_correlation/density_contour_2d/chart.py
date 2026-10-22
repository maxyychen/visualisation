# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(12)
short = rng.multivariate_normal([2.0, 54], [[0.07, 0.3], [0.3, 30]], 350)
long = rng.multivariate_normal([4.3, 80], [[0.17, 0.6], [0.6, 35]], 650)
df = pd.DataFrame(np.vstack([short, long]), columns=["duration_min", "waiting_min"])
df.head()

# %% plot
import seaborn as sns
fig, ax = plt.subplots(figsize=(7.5, 5.5))
sns.kdeplot(data=df, x="duration_min", y="waiting_min", fill=True, cmap=SEQ_CMAP,
            levels=10, thresh=0.03, ax=ax)
sns.kdeplot(data=df, x="duration_min", y="waiting_min", color="#1c5cab",
            levels=10, thresh=0.03, linewidths=0.6, ax=ax)
ax.scatter(df["duration_min"], df["waiting_min"], s=3, color="#0d366b", alpha=0.25)
ax.set_xlabel("Eruption duration (min)")
ax.set_ylabel("Waiting time to next eruption (min)")
ax.set_title("Geyser eruptions form two clusters")
fig.tight_layout()
