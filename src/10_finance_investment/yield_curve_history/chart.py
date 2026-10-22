# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(17)
dates = pd.date_range("2000-01-31", "2025-12-31", freq="ME")
t = dates.year + (dates.month - 1) / 12
anchors_short = {2000: 6.0, 2001.9: 1.8, 2004: 1.0, 2006.5: 5.2, 2008.9: 0.2, 2015.9: 0.2,
                 2019.3: 2.4, 2020.3: 0.1, 2022.0: 0.2, 2023.0: 4.4, 2023.6: 5.4, 2024.6: 5.3, 2025.9: 4.0}
anchors_long = {2000: 6.3, 2003: 4.3, 2007: 4.9, 2012.5: 2.0, 2016: 2.2, 2018.8: 3.1, 2020.5: 1.0,
                2022.0: 1.9, 2023.0: 3.8, 2023.8: 4.8, 2025.9: 4.6}
short = np.interp(t, list(anchors_short), list(anchors_short.values())) + rng.normal(0, 0.06, len(t))
level = np.interp(t, list(anchors_long), list(anchors_long.values())) + rng.normal(0, 0.12, len(t))
curve = rng.normal(0, 0.3, len(t)).cumsum() * 0.05

maturities = ["3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
tau = np.array([0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
lam = 1.8
f1 = (1 - np.exp(-tau / lam)) / (tau / lam)
f2 = f1 - np.exp(-tau / lam)
beta1 = short - level                                 # Nelson-Siegel slope factor
yields = level[:, None] + beta1[:, None] * f1 + curve[:, None] * f2
yields = pd.DataFrame(np.clip(yields, 0.05, None), index=dates, columns=maturities).round(2)
yields["spread_10y_2y"] = yields["10Y"] - yields["2Y"]
yields.iloc[::60]

# %% plot
fig, (ax, axs) = plt.subplots(2, 1, figsize=(11, 6.5), sharex=True,
                              gridspec_kw={"height_ratios": [2.4, 1]})
z = yields[maturities].to_numpy().T
x_edges = yields.index.append(pd.DatetimeIndex([yields.index[-1] + pd.offsets.MonthEnd(1)]))
mesh = ax.pcolormesh(x_edges, np.arange(len(maturities) + 1), z, cmap=SEQ_CMAP, vmin=0, vmax=7)
ax.set_yticks(np.arange(len(maturities)) + 0.5, maturities)
ax.set_ylabel("Maturity")
ax.grid(False)
ax.set_title("Yield curve history, 2000–2025 (simulated)")

s = yields["spread_10y_2y"]
axs.fill_between(s.index, s, 0, where=s >= 0, color=PALETTE[0], alpha=0.75, linewidth=0, interpolate=True)
axs.fill_between(s.index, s, 0, where=s < 0, color=PALETTE[1], alpha=0.85, linewidth=0, interpolate=True)
axs.axhline(0, color="#52514e", linewidth=0.8)
axs.set_ylabel("10Y–2Y (pp)")
axs.text(pd.Timestamp("2016-06-30"), s.max() * 0.8, "orange = inverted curve", color=PALETTE[1], fontsize=9)
axs.grid(axis="x", visible=False)
cb = fig.colorbar(mesh, ax=[ax, axs], fraction=0.025, pad=0.01)
cb.set_label("Yield (%)")
cb.outline.set_visible(False)
