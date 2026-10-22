# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(8)
years = np.arange(2014, 2025)
series = {}
for i in range(12):
    base = rng.uniform(13, 17) + np.cumsum(rng.normal(0, 0.35, len(years)))
    series[f"Region {i + 1}"] = base
series["Region 7"] = 16 - 0.55 * (years - 2014) + rng.normal(0, 0.2, len(years))
df = pd.DataFrame(series, index=years)
df.round(1).head()

# %% plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)

# Misleading: 12 colors, a legend, no focus.
cmap = plt.get_cmap("tab10")
for i, col in enumerate(df.columns):
    ax1.plot(df.index, df[col], color=cmap(i % 10), linewidth=1.6, label=col)
ax1.legend(ncol=2, fontsize=7.5, loc="lower left")
ax1.set_ylabel("Readmission rate (%)")
ax1.set_title("✗ Misleading: 12 colored lines — who improved?", fontsize=11.5)

# Better: gray context, one highlight, the median for reference, direct labels.
for col in df.columns:
    ax2.plot(df.index, df[col], color=GRAY, linewidth=1, alpha=0.7)
med = df.drop(columns="Region 7").median(axis=1)
ax2.plot(df.index, med, color="#52514e", linewidth=1.8)
ax2.plot(df.index, df["Region 7"], color=PALETTE[0], linewidth=2.5)
ax2.text(years[-1] + 0.2, df["Region 7"].iloc[-1], "Region 7", color=PALETTE[0],
         va="center", fontsize=10, fontweight="bold")
ax2.text(years[-1] + 0.2, med.iloc[-1], "Median of\nother regions", color="#52514e",
         va="center", fontsize=9)
ax2.set_xlim(years[0], years[-1] + 2.2)
ax2.set_title("✓ Better: Region 7 cut readmissions; others flat", fontsize=11.5)
fig.tight_layout()
