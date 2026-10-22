# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
maturities = ["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
years = np.array([1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
curves = pd.DataFrame({
    "Normal": [1.50, 1.60, 1.80, 2.00, 2.30, 2.50, 2.80, 3.00, 3.20, 3.50, 3.60],
    "Inverted": [5.50, 5.45, 5.50, 5.40, 4.90, 4.60, 4.30, 4.20, 4.10, 4.35, 4.20],
    "Latest": [4.30, 4.25, 4.15, 4.00, 3.75, 3.70, 3.80, 3.95, 4.15, 4.60, 4.70],
}, index=pd.Index(maturities, name="maturity"))
curves.loc["spread_10y_2y"] = curves.loc["10Y"] - curves.loc["2Y"]
curves.round(2)

# %% plot
yc = curves.drop(index="spread_10y_2y")
x = np.sqrt(years)                                   # sqrt-maturity axis
styles = {"Normal": ("#a9a8a2", 1.6), "Inverted": (PALETTE[1], 2), "Latest": (PALETTE[0], 2.6)}
fig, ax = plt.subplots(figsize=(9.5, 5.5))
inv = yc["Inverted"].to_numpy()
ax.fill_between(x, inv, inv[1], where=inv < inv[1], interpolate=True, color=PALETTE[1],
                alpha=0.15, linewidth=0)
for name, (color, lw) in styles.items():
    y = yc[name].to_numpy()
    ax.plot(x, y, color=color, linewidth=lw, marker="o", markersize=4)
    spread = curves.loc["spread_10y_2y", name] * 100
    ax.text(x[-1] + 0.12, y[-1], f"{name}\n10Y–2Y: {spread:+.0f} bp", color=color if name != "Normal"
            else "#7a7974", va="center", fontsize=9, fontweight="bold")
ax.text(np.sqrt(7), inv[1] - 0.18, "inverted vs 3-month bill", color=PALETTE[1], fontsize=8.5, ha="center")
ax.set_xticks(x, maturities)
ax.set_xlim(x[0] - 0.1, x[-1] + 1.3)
ax.set_ylabel("Yield (%)")
ax.set_xlabel("Maturity (square-root scale)")
ax.set_title("Treasury yield curves (illustrative)")
fig.tight_layout()
