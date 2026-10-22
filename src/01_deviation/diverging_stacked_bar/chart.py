# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
levels = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
questions = ["I feel valued", "Workload is manageable", "Clear career path",
             "Good team communication", "Would recommend employer"]
pct = np.array([[5, 12, 20, 40, 23],
                [14, 26, 22, 28, 10],
                [18, 30, 25, 19, 8],
                [3, 8, 15, 45, 29],
                [6, 14, 24, 35, 21]], dtype=float)
df = pd.DataFrame(pct, index=questions, columns=levels)
df = df.loc[(df["Agree"] + df["Strongly agree"]).sort_values().index]
df

# %% plot
colors = ["#c4462b", "#f0a07f", "#d0cfca", "#86b6ef", "#1c5cab"]
left_start = -(df.iloc[:, 0] + df.iloc[:, 1] + df.iloc[:, 2] / 2)
fig, ax = plt.subplots(figsize=(9, 4.5))
left = left_start.values.copy()
for level, color in zip(df.columns, colors):
    ax.barh(df.index, df[level], left=left, color=color, label=level,
            height=0.65, edgecolor="#fcfcfb", linewidth=1.5)
    left += df[level].values
ax.axvline(0, color="#52514e", linewidth=1)
ax.set_xlim(-70, 85)
ax.set_xticks(range(-60, 81, 20))
ax.set_xticklabels([f"{abs(t)}%" for t in range(-60, 81, 20)])
ax.grid(axis="y", visible=False)
ax.set_title("Employee engagement survey")
ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.45, -0.1), fontsize=8.5)
fig.tight_layout()
