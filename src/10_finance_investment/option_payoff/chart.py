# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from scipy.stats import norm

# %% data
S0, T, r, sigma = 100.0, 0.25, 0.04, 0.25


def black_scholes(S, K, T, r, sigma, kind):
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if kind == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


ST = np.linspace(60, 140, 801)                       # price at expiry


def leg(kind, K, qty):                               # qty: +1 long, -1 short
    premium = black_scholes(S0, K, T, r, sigma, kind)
    payoff = np.maximum(ST - K, 0) if kind == "call" else np.maximum(K - ST, 0)
    return qty * (payoff - premium)


strategies = pd.DataFrame({
    "Long call (K=100)": leg("call", 100, 1),
    "Protective put (stock + put K=95)": (ST - S0) + leg("put", 95, 1),
    "Long straddle (call + put, K=100)": leg("call", 100, 1) + leg("put", 100, 1),
    "Iron condor (85/95/105/115)": leg("put", 85, 1) + leg("put", 95, -1) + leg("call", 105, -1) + leg("call", 115, 1),
}, index=pd.Index(ST, name="price_at_expiry"))
strategies.iloc[::100].round(2)

# %% plot
fig, axes = plt.subplots(2, 2, figsize=(10.5, 7), sharex=True)
for ax, (name, pnl) in zip(axes.flat, strategies.items()):
    x, y = pnl.index.to_numpy(), pnl.to_numpy()
    ax.fill_between(x, y, 0, where=y >= 0, color=PALETTE[0], alpha=0.25, linewidth=0, interpolate=True)
    ax.fill_between(x, y, 0, where=y < 0, color=PALETTE[1], alpha=0.25, linewidth=0, interpolate=True)
    ax.plot(x, y, color="#0b0b0b", linewidth=1.8)
    ax.axhline(0, color="#52514e", linewidth=0.8)
    ax.axvline(S0, color="#a9a8a2", linewidth=1)
    cross = np.flatnonzero(np.diff(np.sign(y)) != 0)
    for i in cross:                                   # linear interpolation of breakevens
        be = x[i] - y[i] * (x[i + 1] - x[i]) / (y[i + 1] - y[i])
        ax.scatter(be, 0, s=36, color="#0b0b0b", zorder=3)
        ax.annotate(f"{be:.1f}", (be, 0), xytext=(0, -14), textcoords="offset points",
                    ha="center", fontsize=8.5, color="#0b0b0b",
                    bbox=dict(boxstyle="round,pad=0.15", fc="#fcfcfb", ec="none"))
    ax.set_title(name, fontsize=10.5)
    ax.grid(axis="x", visible=False)
for ax in axes[1]:
    ax.set_xlabel("Underlying price at expiry ($)")
for ax in axes[:, 0]:
    ax.set_ylabel("Profit / loss per share ($)")
fig.suptitle("Option strategies: profit at expiry (spot $100 = gray line; dots = breakevens)",
             x=0.01, ha="left", fontsize=13, fontweight="bold")
fig.tight_layout()
