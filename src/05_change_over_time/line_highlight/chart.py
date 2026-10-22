# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(21)
years = np.arange(2010, 2025)
regions = [f"Region {i:02d}" for i in range(1, 21)]
base = 8 - 0.25 * (years - 2010) + np.where(years >= 2020, 2.5 * np.exp(-(years - 2020)), 0)
df = pd.DataFrame({r: base + rng.normal(0, 1.0) + rng.normal(0, 0.35, len(years)).cumsum()
                   for r in regions}, index=years)
df["Region 07"] = base - 0.3 * (years - 2010) + 1.8
df.iloc[:, :5]

# %% plot
focus = "Region 07"
peer_median = df.drop(columns=focus).median(axis=1)
fig, ax = plt.subplots(figsize=(9, 4.8))
for col in df.columns.drop(focus):
    ax.plot(df.index, df[col], color=GRAY, linewidth=1, alpha=0.7)
ax.plot(df.index, peer_median, color="#52514e", linewidth=1.5)
ax.plot(df.index, df[focus], color=PALETTE[0], linewidth=2.5)
ax.text(df.index[-1] + 0.2, df[focus].iloc[-1], focus, color=PALETTE[0],
        va="center", fontweight="bold")
ax.text(df.index[-1] + 0.2, peer_median.iloc[-1], "Peer median", color="#52514e", va="center")
ax.set_xlim(df.index[0], df.index[-1] + 2.2)
ax.set_ylabel("Unemployment rate (%)")
ax.set_title("Region 07 cut unemployment faster than its peers")
fig.tight_layout()
