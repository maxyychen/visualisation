# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(6)
years = range(2019, 2025)
months = np.arange(1, 13)
rows = []
for i, y in enumerate(years):
    demand = 300 + 4 * i + 60 * np.cos((months - 1.3) / 12 * 2 * np.pi) ** 2 \
        + 25 * np.exp(-((months - 7.5) / 1.2) ** 2) + rng.normal(0, 6, 12)
    rows += [(y, m, d) for m, d in zip(months, demand)]
df = pd.DataFrame(rows, columns=["year", "month", "demand_gwh"])
df.head()

# %% plot
import calendar
latest = df["year"].max()
fig, ax = plt.subplots(figsize=(9, 4.8))
for y, g in df.groupby("year"):
    is_latest = y == latest
    ax.plot(g["month"], g["demand_gwh"], color=PALETTE[0] if is_latest else GRAY,
            linewidth=2.5 if is_latest else 1, zorder=3 if is_latest else 2)
    if is_latest:
        ax.text(12.15, g["demand_gwh"].iloc[-1], str(y), va="center",
                color=PALETTE[0], fontweight="bold")
ax.text(12.15, df[df["year"] < latest].query("month == 12")["demand_gwh"].mean() - 8,
        f"{df['year'].min()}–{latest - 1}", va="center", fontsize=9, color="#8c8b86")
ax.set_xticks(months, [calendar.month_abbr[m] for m in months])
ax.set_xlim(0.8, 12.8)
ax.set_ylabel("Demand (GWh)")
ax.set_title(f"Monthly electricity demand: {latest} vs. earlier years")
fig.tight_layout()
