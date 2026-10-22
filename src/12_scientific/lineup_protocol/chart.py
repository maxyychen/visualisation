# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(2010)
n = 156  # three years of weekly returns
eps = rng.normal(0, 0.02, n)
real = np.empty(n)
real[0] = eps[0]
for t in range(1, n):  # momentum: this week's return carries over into the next
    real[t] = 0.6 * real[t - 1] + eps[t]
real += 0.001
answer = 15  # position of the real series (keep it secret from your viewers)


def lineup(real_returns, answer, n_panels=20, seed=0):
    """Price paths: the real one at `answer`, the rest from shuffled copies of its returns."""
    g = np.random.default_rng(seed)
    paths = [g.permutation(real_returns) for _ in range(n_panels)]
    paths[answer - 1] = real_returns
    return [100 * np.cumprod(1 + r) for r in paths]


panels = lineup(real, answer)
title = "Which price path is real? The other 19 are shuffled copies of its weekly returns (simulated)"
f"lag-1 autocorrelation of the real returns: {np.corrcoef(real[:-1], real[1:])[0, 1]:.2f}"

# %% plot
fig, axes = plt.subplots(4, 5, figsize=(11, 7.6))
for k, (ax, path) in enumerate(zip(axes.flat, panels), start=1):
    ax.plot(path, color=PALETTE[0], linewidth=1.3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.set_facecolor("#f4f3f0")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.text(0.04, 0.86, str(k), transform=ax.transAxes, fontsize=10, color="#52514e", fontweight="bold")
fig.suptitle(title, x=0.01, ha="left", fontweight="bold", fontsize=12.5)
fig.text(0.99, 0.008, f"Answer: panel {answer} is the real series; the others are permutations of its returns.",
         ha="right", fontsize=7.5, color="#8f8e88")
fig.tight_layout(rect=(0, 0.025, 1, 0.96))

# %% real-data
import plotly.express as px

real = px.data.stocks()["AAPL"].pct_change().dropna().to_numpy()
answer = 7
panels = lineup(real, answer)
title = "Which is Apple's real weekly price path (2018–2019)? The other 19 are shuffled copies of its returns"
f"lag-1 autocorrelation of AAPL weekly returns: {np.corrcoef(real[:-1], real[1:])[0, 1]:.2f}"
