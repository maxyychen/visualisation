# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
skills = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical"]
df = pd.DataFrame({"Player A": [88, 85, 72, 86, 38, 70],
                   "Player B": [70, 62, 88, 79, 76, 82]}, index=skills)
title = "Player skill profiles"
df

# %% plot
angles = np.linspace(0, 2 * np.pi, len(df), endpoint=False).tolist()
angles += angles[:1]
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
for i, col in enumerate(df.columns):
    vals = df[col].tolist() + df[col].tolist()[:1]
    ax.plot(angles, vals, color=PALETTE[i], linewidth=2, label=col)
    ax.fill(angles, vals, color=PALETTE[i], alpha=0.15)
ax.set_xticks(angles[:-1], df.index)
ax.set_ylim(0, 100)
ax.set_yticks([25, 50, 75, 100], ["25", "50", "75", "100"], color="#8c8b86", fontsize=8)
ax.spines["polar"].set_color("#c9c8c3")
ax.set_title(title, pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.08))
fig.tight_layout()

# %% real-data
from sklearn.datasets import load_wine
w = load_wine(as_frame=True).frame
feats = {"alcohol": "Alcohol", "malic_acid": "Malic acid", "flavanoids": "Flavanoids",
         "color_intensity": "Colour intensity", "hue": "Hue", "proline": "Proline"}
means = w.groupby("target")[list(feats)].mean().rename(columns=feats)
df = (means / means.max() * 100).T.round(0)          # % of the highest cultivar mean
df.columns = [f"Cultivar {i + 1}" for i in df.columns]
title = "Wine cultivars (% of highest mean)"
df
