# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(12)
dates = pd.bdate_range("2019-01-01", "2024-12-31")
n = len(dates)
t = np.arange(n)
noise = rng.normal(0, 0.022, n)
# convenience yield: low in a glut (2020), high in a squeeze (2022), mean-reverting noise
conv = 0.04 + 0.10 * np.exp(-((t - 330) / 60.0) ** 2) * -1.2 + 0.16 * np.exp(-((t - 900) / 120.0) ** 2)
conv = conv + np.convolve(rng.normal(0, 0.01, n), np.ones(20) / 20, mode="same")
spot = 60 * np.exp(0.3 * np.cumsum(noise) + 3 * (conv - 0.04))   # cheap in a glut, dear in a squeeze
r = 0.03
months = np.arange(1, 13)
curves = pd.DataFrame(spot[:, None] * np.exp((r - conv[:, None]) * months[None, :] / 12),
                      index=dates, columns=[f"M{m}" for m in months])
spread = (curves["M12"] / curves["M1"] - 1).rename("12M − 1M spread")
show_dates = [pd.Timestamp(d) for d in ("2019-06-03", "2020-04-20", "2022-06-14", "2024-06-03")]
curves.loc[curves.index.isin(show_dates)].round(1)

# %% plot
date_colors = [PALETTE[2], PALETTE[3], PALETTE[4], PALETTE[6]]   # not blue/orange: those mean contango/backwardation
fig, (ax_c, ax_s) = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw={"width_ratios": [1, 1.5], "wspace": 0.22})
ends, label_y = [], {}
for d in show_dates:
    d = curves.index[curves.index.get_indexer([d], method="nearest")[0]]
    ends.append((curves.loc[d].iloc[-1], d))
last = -np.inf
for v, d in sorted(ends):                       # keep end labels at least 6 $ apart
    label_y[d] = max(v, last + 6)
    last = label_y[d]
for k, d in enumerate(show_dates):
    d = curves.index[curves.index.get_indexer([d], method="nearest")[0]]
    row = curves.loc[d]
    ax_c.plot(months, row.values, color=date_colors[k], marker="o", markersize=3.5)
    shape = "contango" if row.iloc[-1] > row.iloc[0] else "backwardation"
    ax_c.annotate(f"{d:%b %Y}\n{shape}", (months[-1], row.iloc[-1]), xytext=(12.4, label_y[d]),
                  textcoords="data", va="center", fontsize=8.5, color=date_colors[k],
                  arrowprops=dict(arrowstyle="-", color=date_colors[k], linewidth=0.6, shrinkA=0, shrinkB=2))
    ax_s.scatter(d, spread.loc[d], color=date_colors[k], s=45, zorder=4, edgecolor="#fcfcfb", linewidth=1.5)
ax_c.set_xticks(months)
ax_c.set_xlim(0.5, 15.5)
ax_c.set_xlabel("Months to expiry")
ax_c.set_ylabel("Futures price ($/bbl)")
ax_c.set_title("Futures curves on four dates", fontsize=11)

ax_s.fill_between(spread.index, spread, 0, where=spread >= 0, color=PALETTE[0], alpha=0.35,
                  interpolate=True, linewidth=0, label="Contango")
ax_s.fill_between(spread.index, spread, 0, where=spread < 0, color=PALETTE[1], alpha=0.35,
                  interpolate=True, linewidth=0, label="Backwardation")
ax_s.plot(spread.index, spread, color="#52514e", linewidth=0.9)
ax_s.axhline(0, color="#52514e", linewidth=1)
ax_s.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:+.0%}"))
ax_s.set_ylabel("12-month minus front-month, % of front")
ax_s.set_title("Curve slope over time", fontsize=11)
ax_s.legend(loc="lower left", fontsize=9)
fig.suptitle("Crude-oil futures: contango in the glut, backwardation in the squeeze (simulated)",
             x=0.06, ha="left", fontsize=14, fontweight="bold")
