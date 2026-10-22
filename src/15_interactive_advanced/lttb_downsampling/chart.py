# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(5)
N = 1_500_000                                   # ticks in one trading session
t = np.linspace(9.5, 16.0, N)                   # hours, 09:30 -> 16:00
steps = rng.standard_t(3, N) * 0.000008       # ~1.5% daily volatility
price = 100 * np.exp(np.cumsum(steps)) * (1 + rng.normal(0, 0.00008, N))   # + bid-ask bounce
crash = int(N * 0.62)                           # a flash crash: -5% in ~300 ticks, slow recovery
price[crash:crash + 300] *= np.linspace(1, 0.95, 300)
price[crash + 300:crash + 6300] *= np.linspace(0.95, 1, 6000)
for k in rng.choice(N, 4, replace=False):       # a few single-tick bad prints
    price[k] *= 1 + rng.choice([-1, 1]) * 0.02
df = pd.DataFrame({"hour": t, "price": price})
print(f"{len(df):,} ticks, low {price.min():.2f} at {t[price.argmin()]:.3f} h")

# %% plot
def every_nth(x, y, n_out):
    return np.linspace(0, len(x) - 1, n_out).astype(int)


def lttb(x, y, n_out):
    """Largest-Triangle-Three-Buckets (Steinarsson 2013): per bucket, keep the point that forms
    the largest triangle with the previously kept point and the next bucket's average."""
    n = len(x)
    if n_out >= n:
        return np.arange(n)
    edges = np.floor(np.linspace(1, n - 1, n_out - 1)).astype(int)   # n_out-2 interior buckets
    keep = np.empty(n_out, dtype=int)
    keep[0], keep[-1] = 0, n - 1
    a = 0
    for i in range(n_out - 2):
        lo, hi = edges[i], edges[i + 1]
        nlo, nhi = hi, (edges[i + 2] if i + 2 < len(edges) else n)
        cx, cy = x[nlo:nhi].mean(), y[nlo:nhi].mean()
        area = np.abs((x[a] - cx) * (y[lo:hi] - y[a]) - (x[a] - x[lo:hi]) * (cy - y[a]))
        a = lo + int(np.argmax(area))
        keep[i + 1] = a
    return keep


def minmax_lttb(x, y, n_out, ratio=4):
    """MinMaxLTTB (Van Der Donckt et al. 2023): keep each small bucket's min and max first
    (vectorised, cheap), then run LTTB on that much smaller candidate set."""
    n_buckets = n_out * ratio // 2
    usable = (len(x) - 2) // n_buckets * n_buckets
    block = y[1:1 + usable].reshape(n_buckets, -1)
    offs = np.arange(n_buckets) * block.shape[1] + 1
    cand = np.unique(np.concatenate([[0], offs + block.argmin(1), offs + block.argmax(1), [len(x) - 1]]))
    return cand[lttb(x[cand], y[cand], n_out)]


x, y = df["hour"].to_numpy(), df["price"].to_numpy()
N_OUT = 1_000
methods = {}
for name, fn in (("Every n-th point", every_nth), ("LTTB", lttb), ("MinMaxLTTB", minmax_lttb)):
    methods[name] = fn(x, y, N_OUT)   # time these with %timeit: MinMaxLTTB is several times faster

true_low = y.min()
zoom = (x[crash] - 0.06, x[crash] + 0.12)
fig, axes = plt.subplots(4, 2, figsize=(14, 10), sharex="col", sharey="row",
                         gridspec_kw={"width_ratios": [2.2, 1]})
rows = [("Full resolution", np.arange(len(x)))] + list(methods.items())
for r, (name, idx) in enumerate(rows):
    color = "#52514e" if r == 0 else (PALETTE[1] if name == "Every n-th point" else PALETTE[0])
    for c in range(2):
        ax = axes[r, c]
        ax.plot(x[idx], y[idx], color=color, linewidth=0.7 if r == 0 else 1.1, rasterized=(r == 0))
        if r > 0:
            ax.axhline(true_low, color="#b8b7b1", linewidth=0.8, zorder=0)
        if c == 1:
            ax.set_xlim(*zoom)
    low = y[idx].min()
    caught = "keeps" if abs(low - true_low) / true_low < 0.002 else "misses"
    label = (f"{name}: {len(idx):,} points" if r == 0 else
             f"{name}: {len(idx):,} points · {caught} the crash low ({low:.2f} vs {true_low:.2f})")
    axes[r, 0].set_title(label, fontsize=11)
    axes[r, 0].set_ylabel("Price")
axes[0, 1].set_title("Zoom: the flash crash", fontsize=11)
for ax in axes[-1]:
    ax.set_xlabel("Hour of the trading day")
fig.suptitle("Drawing 1.5 million ticks with 1,000 points: naive decimation vs. LTTB vs. MinMaxLTTB (simulated)",
             x=0.01, ha="left", fontsize=13.5, fontweight="bold")
fig.tight_layout()
