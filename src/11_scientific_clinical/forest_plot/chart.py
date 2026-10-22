# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rows = [  # label, HR, lower, upper, n   (None = section header)
    ("Overall", 0.72, 0.60, 0.86, 840),
    ("Age", None, None, None, None),
    ("  < 65 years", 0.68, 0.53, 0.87, 470), ("  ≥ 65 years", 0.78, 0.59, 1.03, 370),
    ("Sex", None, None, None, None),
    ("  Female", 0.70, 0.54, 0.91, 410), ("  Male", 0.74, 0.57, 0.96, 430),
    ("ECOG status", None, None, None, None),
    ("  0", 0.65, 0.50, 0.85, 500), ("  1", 0.83, 0.62, 1.11, 340),
    ("Biomarker", None, None, None, None),
    ("  Positive", 0.55, 0.42, 0.72, 380), ("  Negative", 0.92, 0.72, 1.18, 460),
]
df = pd.DataFrame(rows, columns=["label", "hr", "lo", "hi", "n"])
df

# %% plot
fig, ax = plt.subplots(figsize=(9, 6))
y = np.arange(len(df))[::-1]
for yi, r in zip(y, df.itertuples()):
    if pd.isna(r.hr):
        continue
    if r.label == "Overall":
        ax.fill([r.lo, r.hr, r.hi, r.hr], [yi, yi + 0.3, yi, yi - 0.3], color=PALETTE[0])
    else:
        ax.hlines(yi, r.lo, r.hi, color="#52514e", linewidth=1.2)
        ax.scatter(r.hr, yi, marker="s", s=r.n / 4, color=PALETTE[0], zorder=3)
    ax.text(1.03, yi, f"{r.hr:.2f} ({r.lo:.2f}–{r.hi:.2f})", transform=ax.get_yaxis_transform(),
            va="center", fontsize=9)
ax.axvline(1, color="#52514e", linewidth=1)
ax.set_xscale("log")
ax.set_xticks([0.4, 0.6, 0.8, 1, 1.25], ["0.4", "0.6", "0.8", "1", "1.25"])
ax.minorticks_off()
ax.set_xlim(0.35, 1.4)
ax.set_yticks(y, df["label"])
for lab, is_hdr in zip(ax.get_yticklabels(), df["hr"].isna()):
    if is_hdr:
        lab.set_fontweight("bold")
ax.grid(axis="y", visible=False)
ax.text(1.03, len(df) - 0.2, "HR (95% CI)", transform=ax.get_yaxis_transform(), fontweight="bold", fontsize=9)
ax.set_xlabel("← favours new treatment     Hazard ratio     favours control →")
ax.set_title("Overall survival by subgroup")
fig.tight_layout()
