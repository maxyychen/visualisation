# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

# %% data
fcf = np.array([600, 650, 700, 740, 780.0])        # $m, years 1..5
net_debt, shares, price_now = 1800.0, 250.0, 38.50
waccs = np.round(np.arange(0.075, 0.1051, 0.005), 4)
growths = np.round(np.arange(0.010, 0.0301, 0.005), 4)


def value_per_share(wacc, g):
    t = np.arange(1, len(fcf) + 1)
    pv_fcf = (fcf / (1 + wacc) ** t).sum()
    terminal = fcf[-1] * (1 + g) / (wacc - g)       # Gordon growth, value at end of year 5
    ev = pv_fcf + terminal / (1 + wacc) ** len(fcf)
    return (ev - net_debt) / shares


table = pd.DataFrame([[value_per_share(w, g) for w in waccs] for g in growths],
                     index=[f"{g:.1%}" for g in growths], columns=[f"{w:.1%}" for w in waccs]).round(2)
base = ("2.0%", "8.5%")                             # (growth, WACC)
table

# %% plot
cmap = LinearSegmentedColormap.from_list("down_up", [PALETTE[1], "#e3e2de", PALETTE[0]])
z = table.to_numpy()
norm = TwoSlopeNorm(vmin=min(z.min(), price_now * 0.6), vcenter=price_now, vmax=max(z.max(), price_now * 1.4))
fig, ax = plt.subplots(figsize=(10, 4.8))
im = ax.imshow(z, cmap=cmap, norm=norm, aspect="auto")
for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        v = z[i, j]
        far = abs(norm(v) - 0.5) > 0.32
        ax.text(j, i - 0.12, f"${v:.1f}", ha="center", va="center", fontsize=10, fontweight="bold",
                color="white" if far else "#0b0b0b")
        ax.text(j, i + 0.22, f"{v / price_now - 1:+.0%}", ha="center", va="center", fontsize=8,
                color="white" if far else "#52514e")
bi, bj = table.index.get_loc(base[0]), table.columns.get_loc(base[1])
ax.add_patch(plt.Rectangle((bj - 0.5, bi - 0.5), 1, 1, fill=False, edgecolor="#0b0b0b", linewidth=2.2))
ax.set_xticks(range(len(waccs)), table.columns)
ax.set_yticks(range(len(growths)), table.index)
ax.set_xlabel("Discount rate (WACC)")
ax.set_ylabel("Terminal growth")
ax.xaxis.set_label_position("top")
ax.xaxis.tick_top()
ax.grid(False)
for sp in ax.spines.values():
    sp.set_visible(False)
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
cb.set_label(f"Value per share (\\$); gray = current \\${price_now:.2f}")
cb.outline.set_visible(False)
ax.set_title("DCF value per share: sensitivity to WACC and terminal growth (base case outlined)", pad=32)
fig.tight_layout()
