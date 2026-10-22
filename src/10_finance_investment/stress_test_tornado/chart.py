# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame({
    "factor":   ["Equity markets", "Interest rates", "Credit spreads", "USD exchange rate",
                 "Oil price", "Inflation", "Equity volatility", "Real estate"],
    "down_shock": ["−20%", "+100 bp", "+150 bp", "USD +10%", "−30%", "+2 pp", "VIX +15", "−15%"],
    "up_shock":   ["+20%", "−100 bp", "−75 bp", "USD −10%", "+30%", "−1 pp", "VIX −5", "+15%"],
    "down_pnl": [-11.8, -4.6, -3.9, -2.4, -1.1, -1.6, -2.9, -1.4],   # P&L, $ millions
    "up_pnl":   [10.9, 4.1, 1.8, 2.2, 0.9, 0.7, 0.8, 1.3],
})
df["range"] = df["up_pnl"] - df["down_pnl"]
df = df.sort_values("range").reset_index(drop=True)
df

# %% plot
fig, ax = plt.subplots(figsize=(9, 5))
y = np.arange(len(df))
ax.barh(y, df["down_pnl"], color=PALETTE[1], height=0.65, label="Downside shock")
ax.barh(y, df["up_pnl"], color=PALETTE[0], height=0.65, label="Upside shock")
for yi, row in df.iterrows():
    ax.text(row["down_pnl"] - 0.25, yi, f"{row['down_shock']}  {row['down_pnl']:+.1f}", ha="right",
            va="center", fontsize=8.5, color="#52514e")
    ax.text(row["up_pnl"] + 0.25, yi, f"{row['up_pnl']:+.1f}  {row['up_shock']}", ha="left",
            va="center", fontsize=8.5, color="#52514e")
ax.axvline(0, color="#52514e", linewidth=1)
ax.set_yticks(y, df["factor"])
lim = df[["down_pnl", "up_pnl"]].abs().max().max() * 1.55
ax.set_xlim(-lim, lim)
ax.set_xlabel("Portfolio P&L vs. base case ($ millions)")
ax.set_title("Stress test: which shocks move the portfolio most")
ax.grid(axis="y", visible=False)
ax.legend(loc="lower right")
fig.tight_layout()
