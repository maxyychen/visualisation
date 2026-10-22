# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from scipy import stats
from matplotlib.ticker import PercentFormatter

# %% data
rng = np.random.default_rng(8)
r = pd.Series(0.0004 + rng.standard_t(5, 2520) * 0.01 * np.sqrt(3 / 5), name="Fund daily returns")
horizon = "one-day"
r.describe()

# %% real-data
import plotly.express as px
stocks = px.data.stocks()
r = stocks["FB"].pct_change().dropna().rename("FB weekly returns")
horizon = "one-week"
r.describe()

# %% plot
var95, var99 = np.quantile(r, [0.05, 0.01])
cvar95 = r[r <= var95].mean()
mu, sd = r.mean(), r.std()
xs = np.linspace(r.min() * 1.1, r.max() * 1.1, 400)
bins = np.linspace(r.min(), r.max(), 60 if len(r) > 500 else 25)

fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1.5, 1]})
for a in (ax, ax2):
    a.hist(r, bins=bins, density=True, color=PALETTE[0], alpha=0.75, edgecolor="#fcfcfb", linewidth=0.5)
    a.plot(xs, stats.norm.pdf(xs, mu, sd), color="#52514e", linewidth=1.5, label="Normal fit")
    a.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0 if r.abs().max() > 0.1 else 1))
for v, lab, style in [(var95, f"VaR 95% = {var95:.2%}", "-"), (var99, f"VaR 99% = {var99:.2%}", "--"),
                      (cvar95, f"CVaR 95% = {cvar95:.2%}", ":")]:
    ax.axvline(v, color=PALETTE[1], linewidth=1.6, linestyle=style, label=lab)
lo, hi = np.quantile(r, [0.002, 0.998])
ax.set_xlim(lo * 1.4, hi * 1.4)
ax.axvspan(lo * 1.4, var95, color=PALETTE[1], alpha=0.08, linewidth=0)
ax.set_title(f"{r.name}: distribution and {horizon} VaR")
ax.set_xlabel("Return")
ax.set_ylabel("Density")
ax.legend(loc="upper right", fontsize=8.5)
ax2.set_yscale("log")
ax2.set_ylim(bottom=0.5 / (len(r) * (bins[1] - bins[0])))
ax2.set_title("Same data, log density: fat tails")
ax2.set_xlabel("Return")
k = stats.kurtosis(r)
ax2.text(0.03, 0.97, f"excess kurtosis = {k:.1f}\n(normal = 0)", transform=ax2.transAxes, va="top",
         fontsize=9, color="#52514e")
fig.tight_layout()
