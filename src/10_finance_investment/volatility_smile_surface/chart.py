# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
S0, r = 100.0, 0.04
expiries = {"1M": 1 / 12, "3M": 0.25, "6M": 0.5, "1Y": 1.0, "2Y": 2.0}
strikes = np.arange(70, 131, 5)


def implied_vol(K, T):
    k = np.log(K / (S0 * np.exp(r * T)))             # log-moneyness vs forward
    atm = 0.16 + 0.04 * (1 - np.exp(-T))
    skew = -0.12 / np.sqrt(T)
    curvature = 0.25 / np.sqrt(T)
    return np.maximum(atm + skew * k + curvature * k ** 2, 0.05)


iv = pd.DataFrame({name: implied_vol(strikes, T) * 100 for name, T in expiries.items()},
                  index=pd.Index(strikes, name="strike")).round(1)
iv.T

# %% plot
ramp = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]   # ordinal: near -> far
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1.1, 1]})
for (name, col), color in zip(iv.items(), ramp):
    ax1.plot(iv.index, col, color=color, linewidth=2, marker="o", markersize=3.5)
    ax1.text(iv.index[-1] + 1, col.iloc[-1], name, color=color, va="center", fontsize=9, fontweight="bold")
ax1.axvline(S0, color="#a9a8a2", linewidth=1)
ax1.text(S0 + 0.5, ax1.get_ylim()[1] * 0.98, "spot", color="#7a7974", fontsize=8.5, va="top")
ax1.set_xlim(iv.index[0] - 2, iv.index[-1] + 7)
ax1.set_xlabel("Strike ($)")
ax1.set_ylabel("Implied volatility (%)")
ax1.set_title("Smile by expiry")

z = iv.T.to_numpy()
im = ax2.imshow(z, cmap=SEQ_CMAP, aspect="auto", origin="upper")
for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        ax2.text(j, i, f"{z[i, j]:.0f}", ha="center", va="center", fontsize=7.5,
                 color="white" if z[i, j] > np.percentile(z, 70) else "#0b0b0b")
ax2.set_xticks(range(len(strikes)), strikes, fontsize=8)
ax2.set_yticks(range(len(expiries)), list(expiries))
ax2.set_xlabel("Strike ($)")
ax2.set_title("Surface (implied vol, %)")
ax2.grid(False)
for sp in ax2.spines.values():
    sp.set_visible(False)
cb = fig.colorbar(im, ax=ax2, fraction=0.04, pad=0.02)
cb.outline.set_visible(False)
fig.suptitle("Equity implied volatility: downside strikes are priced richer (simulated)",
             x=0.01, ha="left", fontsize=13, fontweight="bold")
fig.tight_layout()
