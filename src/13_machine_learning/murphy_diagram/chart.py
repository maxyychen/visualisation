# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(8)
n = 600  # months
log_level = np.zeros(n)
for t in range(1, n):
    log_level[t] = 0.92 * log_level[t - 1] + rng.normal(0, 0.18)
sigma = 16 * np.exp(log_level)                         # latent volatility regime (% annualised)
noise_sd = 0.25
realised = sigma * np.exp(rng.normal(0, noise_sd, n))  # next month's realised volatility
cond_mean = sigma * np.exp(noise_sd ** 2 / 2)
model_a = cond_mean * np.exp(rng.normal(0, 0.08, n))                       # tracks the regime
model_b = 0.3 * cond_mean + 0.7 * realised.mean() + rng.normal(0, 0.3, n)  # shrinks to the average
df = pd.DataFrame({"realised": realised, "model_a": model_a, "model_b": model_b})
df.describe().round(1)

# %% plot
def elementary_scores(x, y, theta):
    """Elementary score for the mean (expectile at level 1/2), one column per threshold."""
    X, Y, T = x[:, None], y[:, None], theta[None, :]
    return np.abs((Y < X) - 0.5) * (np.maximum(Y - T, 0) - np.maximum(X - T, 0) - (Y - X) * (T < X))

y = df["realised"].to_numpy()
theta = np.linspace(np.percentile(y, 0.5) * 0.8, np.percentile(y, 99.5) * 1.1, 200)
score_a = elementary_scores(df["model_a"].to_numpy(), y, theta)
score_b = elementary_scores(df["model_b"].to_numpy(), y, theta)
diff = score_a - score_b

# 90% pointwise band from a moving-block bootstrap (12-month blocks keep the autocorrelation).
rng_boot = np.random.default_rng(3)
block = 12
starts = rng_boot.integers(0, n - block, size=(400, n // block))
boot = np.array([diff[(s[:, None] + np.arange(block)).ravel()].mean(0) for s in starts])
lo, hi = np.quantile(boot, [0.05, 0.95], axis=0)

fig, (ax, axd) = plt.subplots(2, 1, figsize=(9, 7), sharex=True, height_ratios=[1.4, 1])
ax.plot(theta, score_a.mean(0), color=PALETTE[0], label="Model A: tracks the regime")
ax.plot(theta, score_b.mean(0), color=PALETTE[1], label="Model B: shrinks to the average")
ax.set_ylabel("Mean elementary score\n(lower is better)")
better, worse = hi < 0, lo > 0
ax.set_title(f"Murphy diagram: Model A reliably better at {better.mean():.0%} of thresholds, "
             f"reliably worse at {worse.mean():.0%}")
ax.legend(loc="upper right")

axd.fill_between(theta, lo, hi, color="#d0cfca", alpha=0.8, linewidth=0, label="90% block-bootstrap band")
axd.plot(theta, diff.mean(0), color=PALETTE[0], linewidth=1.8, label="A − B")
axd.fill_between(theta, axd.get_ylim()[0], 0, where=better, color=PALETTE[0], alpha=0.08,
                 linewidth=0, label="A reliably better")
axd.axhline(0, color="#52514e", linewidth=1)
axd.set_xlabel("Decision threshold θ: realised volatility (% annualised)")
axd.set_ylabel("Score difference")
axd.legend(loc="lower right", fontsize=9)
fig.tight_layout()
