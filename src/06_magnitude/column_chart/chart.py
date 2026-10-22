# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame({
    "quarter": ["Q1 23", "Q2 23", "Q3 23", "Q4 23", "Q1 24", "Q2 24", "Q3 24", "Q4 24"],
    "revenue_m": [4.2, 4.8, 5.1, 6.3, 5.0, 5.6, 6.1, 7.4],
})
df

# %% plot
fig, ax = plt.subplots(figsize=(8, 4.5))
colors = [PALETTE[0] if i == len(df) - 1 else "#9ec5f4" for i in range(len(df))]
bars = ax.bar(df["quarter"], df["revenue_m"], color=colors, width=0.65)
ax.bar_label(bars, fmt="$%.1fM", padding=3, fontsize=9, color="#52514e")
ax.set_ylabel("Revenue ($M)")
ax.set_ylim(0, df["revenue_m"].max() * 1.15)
ax.grid(axis="x", visible=False)
ax.set_title("Quarterly revenue: Q4 2024 is a record")
fig.tight_layout()
