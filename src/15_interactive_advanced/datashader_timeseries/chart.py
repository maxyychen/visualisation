# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
import datashader as ds
from matplotlib.colors import LogNorm

# %% data
rng = np.random.default_rng(12)
n_paths, n_days = 2000, 252
dt = 1 / 252
mu, sigma = 0.08, 0.16
shocks = rng.normal((mu - sigma**2 / 2) * dt, sigma * np.sqrt(dt), (n_paths, n_days))
crash = rng.random(n_paths) < 0.15                          # crash regime from day ~90
shocks[crash, 90:120] += rng.normal(-0.014, 0.004, (crash.sum(), 30))   # ~-35% over six weeks
paths = 100 * np.exp(np.cumsum(shocks, axis=1))
paths = np.hstack([np.full((n_paths, 1), 100.0), paths])
days = np.arange(n_days + 1)
# Long format, one NaN row between paths so lines are not joined.
x = np.tile(np.append(days, np.nan), n_paths)
y = np.hstack([np.append(p, np.nan) for p in paths])
lines = pd.DataFrame({"day": x, "price": y})
pd.Series(paths[:, -1]).describe(percentiles=[0.05, 0.5, 0.95]).round(1)

# %% plot
x_range, y_range = (0, n_days), (40, 180)
canvas = ds.Canvas(plot_width=900, plot_height=420, x_range=x_range, y_range=y_range)
density = canvas.line(lines, "day", "price", agg=ds.count()).values.astype(float)
density[density == 0] = np.nan

fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(density, origin="lower", extent=[*x_range, *y_range], aspect="auto",
               cmap=SEQ_CMAP, norm=LogNorm(vmin=1, vmax=np.nanmax(density)), interpolation="nearest")
for q, style in [(50, "-"), (5, "--"), (95, "--")]:
    line = np.percentile(paths, q, axis=0)
    ax.plot(days, line, color=PALETTE[1], linewidth=2 if q == 50 else 1.2, linestyle=style)
    ax.text(n_days + 2, line[-1], f"{'median' if q == 50 else f'P{q}'} {line[-1]:.0f}",
            va="center", fontsize=9, color="#0b0b0b")
ax.set_xlim(*x_range)
ax.set_ylim(*y_range)
ax.grid(False)
ax.set_xlabel("Trading day")
ax.set_ylabel("Price (start = 100)")
ax.set_title(f"{n_paths:,} simulated price paths as a line-density image")
fig.colorbar(im, ax=ax, label="Paths per pixel", pad=0.09)
fig.tight_layout()
