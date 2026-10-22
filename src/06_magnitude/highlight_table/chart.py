# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(23)
products = ["Laptops", "Tablets", "Phones", "Monitors", "Headsets", "Keyboards"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
base = np.array([120, 80, 300, 90, 150, 60])[:, None]
season = np.array([0.9, 0.85, 1.0, 1.05, 1.1, 1.25])[None, :]
df = pd.DataFrame((base * season * rng.uniform(0.85, 1.15, (6, 6))).round().astype(int),
                  index=products, columns=months)
df

# %% plot
import seaborn as sns
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.heatmap(df, annot=True, fmt="d", cmap=SEQ_CMAP, linewidths=2, linecolor="#fcfcfb",
            cbar_kws={"label": "Units sold", "shrink": 0.8}, ax=ax, annot_kws={"fontsize": 10})
ax.set_xlabel(""); ax.set_ylabel("")
ax.tick_params(length=0)
ax.set_title("Units sold by product and month")
fig.tight_layout()
