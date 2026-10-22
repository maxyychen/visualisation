# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

# %% data
rng = np.random.default_rng(21)
dates = pd.bdate_range("2015-01-01", "2024-12-31")
n = len(dates)
r = 0.00045 + rng.standard_t(4, n) * 0.0095 / np.sqrt(2)
r[(dates >= "2020-02-20") & (dates <= "2020-03-23")] -= 0.012
r[(dates >= "2022-01-01") & (dates <= "2022-10-15")] -= 0.0011
daily = pd.Series(r, index=dates)
monthly = (1 + daily).resample("ME").prod() - 1   # simple monthly returns
name = "Fund"
monthly.tail()

# %% real-data
import plotly.express as px
stocks = px.data.stocks().set_index("date")
px_m = pd.Series(stocks["MSFT"].values, index=pd.to_datetime(stocks.index)).resample("ME").last()
monthly = px_m.pct_change().dropna()
name = "MSFT"
monthly.tail()

# %% plot
table = pd.DataFrame({"year": monthly.index.year, "month": monthly.index.month, "r": monthly.values})
grid = table.pivot(index="year", columns="month", values="r").reindex(columns=range(1, 13))
annual = table.groupby("year")["r"].apply(lambda x: (1 + x).prod() - 1)

cmap = LinearSegmentedColormap.from_list("loss_gain", ["#b3471c", "#eb6834", "#f2f1ee", "#2a78d6", "#1c5cab"])
lim = np.nanmax(np.abs(grid.values))
fig, (ax, axy) = plt.subplots(1, 2, figsize=(11, 0.5 * len(grid) + 1.6), sharey=True,
                              gridspec_kw={"width_ratios": [12, 1.4], "wspace": 0.04})
ax.imshow(grid.values, cmap=cmap, norm=TwoSlopeNorm(0, -lim, lim), aspect="auto")
alim = np.abs(annual.values).max()
axy.imshow(annual.values[:, None], cmap=cmap, norm=TwoSlopeNorm(0, -alim, alim), aspect="auto")

def label(axis, values, scale):
    for (i, j), v in np.ndenumerate(values):
        if not np.isnan(v):
            axis.text(j, i, f"{v:+.1%}", ha="center", va="center", fontsize=8,
                      color="white" if abs(v) > 0.6 * scale else "#0b0b0b")

label(ax, grid.values, lim)
label(axy, annual.values[:, None], alim)
ax.set_xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.set_yticks(range(len(grid)), grid.index)
axy.set_xticks([0], ["Year"])
for a in (ax, axy):
    a.grid(False)
    a.tick_params(length=0)
    for s in a.spines.values():
        s.set_visible(False)
    a.xaxis.tick_top()
ax.set_title(f"{name}: monthly returns", pad=28)
fig.tight_layout()
