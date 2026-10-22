# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.isotonic import IsotonicRegression
from sklearn.calibration import calibration_curve

# %% data
rng = np.random.default_rng(21)
n = 3000
# Simulated credit book: true default risk comes from a latent score; the model over-reacts to it.
score = rng.normal(0, 1, n)
true_pd = 1 / (1 + np.exp(-(-2.2 + 1.1 * score)))
default = rng.binomial(1, true_pd)
pred_pd = 1 / (1 + np.exp(-(-2.5 + 1.8 * score + rng.normal(0, 0.25, n))))
df = pd.DataFrame({"pred_pd": pred_pd, "default": default})
df.describe().round(3)

# %% plot
order = np.argsort(df["pred_pd"].to_numpy())
p = df["pred_pd"].to_numpy()[order]
y = df["default"].to_numpy()[order]

def pav(x, outcome):
    return IsotonicRegression(y_min=0, y_max=1, out_of_bounds="clip").fit(x, outcome)

cep = pav(p, y).predict(p)  # CORP: conditional event probability from pool-adjacent-violators

# 90% consistency band: refit PAV on outcomes drawn from a perfectly calibrated model (y* ~ Bernoulli(p)).
rng_band = np.random.default_rng(7)
grid = np.linspace(p.min(), p.max(), 200)
sims = np.array([pav(p, rng_band.binomial(1, p)).predict(grid) for _ in range(300)])
band_lo, band_hi = np.quantile(sims, [0.05, 0.95], axis=0)

# CORP decomposition of the Brier score: S = MCB - DSC + UNC
S = np.mean((p - y) ** 2)
S_cal = np.mean((cep - y) ** 2)
S_ref = np.mean((y.mean() - y) ** 2)
MCB, DSC, UNC = S - S_cal, S_ref - S_cal, S_ref

fig, axes = plt.subplots(2, 2, figsize=(12, 7.2), height_ratios=[3, 1], sharex="col")
ax, ax2 = axes[0]
for a in (ax, ax2):
    a.plot([0, 1], [0, 1], color=GRAY, linewidth=1)
    a.set_xlim(0, 1)
    a.set_ylim(0, 1)

ax.fill_between(grid, band_lo, band_hi, color="#d0cfca", alpha=0.7, linewidth=0,
                label="90% consistency band (calibrated model)")
ax.step(p, cep, where="post", color=PALETTE[0], linewidth=2.2, label="CORP (isotonic / PAV fit)")
ax.set_ylabel("Observed default frequency (CEP)")
ax.set_title("CORP: bins chosen by the data")
ax.text(0.98, 0.04,
        f"Brier {S:.4f} = MCB {MCB:.4f} − DSC {DSC:.4f} + UNC {UNC:.4f}\n"
        "MCB miscalibration · DSC discrimination · UNC uncertainty",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5, color="#52514e")
ax.legend(loc="upper left", fontsize=9)

for color, (label, n_bins, strategy) in zip(
        PALETTE, [("10 equal-width bins", 10, "uniform"), ("10 equal-count bins", 10, "quantile"),
                  ("7 equal-width bins", 7, "uniform")]):
    frac, mean_pred = calibration_curve(y, p, n_bins=n_bins, strategy=strategy)
    ax2.plot(mean_pred, frac, "o-", color=color, markersize=5, linewidth=1.6, label=label,
             markeredgecolor="#fcfcfb", markeredgewidth=1)
ax2.set_title("Classic binned curves: shape depends on the bins")
ax2.legend(loc="upper left", fontsize=9)

for a in axes[1]:
    a.hist(p, bins=np.linspace(0, 1, 41), color=PALETTE[0], alpha=0.55, edgecolor="#fcfcfb", linewidth=0.5)
    a.set_xlabel("Predicted default probability")
    a.set_ylabel("Loans")
    a.grid(axis="x", visible=False)
fig.tight_layout()
