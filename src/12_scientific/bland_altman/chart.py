# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(9)
true_sbp = rng.normal(128, 18, 150)
method_a = true_sbp + rng.normal(0, 4, 150)
method_b = true_sbp + 3 + 0.06 * (true_sbp - 128) + rng.normal(0, 5, 150)
df = pd.DataFrame({"cuff": method_a.round(1), "arterial": method_b.round(1)})
df["mean"] = (df.cuff + df.arterial) / 2
df["diff"] = df.arterial - df.cuff
bias, sd = df["diff"].mean(), df["diff"].std(ddof=1)
loa = (bias - 1.96 * sd, bias + 1.96 * sd)
print(f"bias = {bias:.2f} mmHg, limits of agreement = {loa[0]:.2f} to {loa[1]:.2f}")
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.scatter(df["mean"], df["diff"], s=28, color=PALETTE[0], alpha=0.75,
           edgecolor="#fcfcfb", linewidth=0.8)
ax.axhline(0, color=GRAY, linewidth=1)
ax.axhline(bias, color="#0b0b0b", linewidth=1.2)
for v in loa:
    ax.axhline(v, color=PALETTE[1], linewidth=1.2)
x_lab = df["mean"].max() + 2
for v, lab in [(bias, f"Mean bias {bias:+.1f}"), (loa[1], f"+1.96 SD {loa[1]:+.1f}"),
               (loa[0], f"−1.96 SD {loa[0]:+.1f}")]:
    ax.text(x_lab, v + 0.3, lab, va="bottom", fontsize=9, color="#0b0b0b")
ax.set_xlim(df["mean"].min() - 3, df["mean"].max() + 22)
ax.set_xlabel("Mean of the two methods (mmHg)")
ax.set_ylabel("Arterial − cuff (mmHg)")
ax.set_title("Bland–Altman: arterial line vs. cuff systolic BP")
fig.tight_layout()
