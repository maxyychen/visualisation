# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.linear_model import LogisticRegression

# %% data
rng = np.random.default_rng(17)
n = 1500
df = pd.DataFrame({
    "age": rng.uniform(35, 85, n).round(),
    "size_cm": rng.gamma(2.2, 1.0, n).clip(0.3, 7).round(1),
    "nodes": rng.poisson(1.6, n).clip(0, 12),
    "grade": rng.choice([1, 2, 3], n, p=[0.25, 0.45, 0.30]),
})
lin = -4.2 + 0.012 * df["age"] + 0.35 * df["size_cm"] + 0.30 * df["nodes"] + 0.55 * df["grade"]
df["recurrence"] = (rng.random(n) < 1 / (1 + np.exp(-lin))).astype(int)
model = LogisticRegression(C=1e6, max_iter=2000).fit(df[["age", "size_cm", "nodes", "grade"]], df["recurrence"])
coef = dict(zip(["age", "size_cm", "nodes", "grade"], model.coef_[0]))
print({k: round(v, 3) for k, v in coef.items()}, "intercept", round(model.intercept_[0], 2))

# %% plot
predictors = [  # (column, label, tick values)
    ("age", "Age (years)", np.arange(40, 81, 20)),
    ("size_cm", "Tumour size (cm)", np.arange(0, 8, 1)),
    ("nodes", "Positive lymph nodes", np.arange(0, 13, 2)),
    ("grade", "Histological grade", np.array([1, 2, 3])),
]
lo = {c: (ticks.min() if coef[c] > 0 else ticks.max()) for c, _, ticks in predictors}
span = {c: abs(coef[c]) * (ticks.max() - ticks.min()) for c, _, ticks in predictors}
scale = 100 / max(span.values())                         # largest effect -> 100 points
points = lambda c, v: abs(coef[c] * (v - lo[c])) * scale
total_max = sum(points(c, t.max() if coef[c] > 0 else t.min()) for c, _, t in predictors)
base_lp = model.intercept_[0] + sum(coef[c] * lo[c] for c, _, _ in predictors)
prob_of_total = lambda T: 1 / (1 + np.exp(-(base_lp + T / scale)))

patient = {"age": 62, "size_cm": 3.0, "nodes": 4, "grade": 3}
pt_points = {c: points(c, patient[c]) for c in patient}
pt_total = sum(pt_points.values())

fig, ax = plt.subplots(figsize=(10, 6.2))
ax.axis("off")
rows = len(predictors) + 3
y = lambda r: rows - r
def scale_row(r, label, positions, labels, minor=None):
    ax.plot([min(positions), max(positions)], [y(r), y(r)], color="#52514e", linewidth=1)
    for p, l in zip(positions, labels):
        ax.plot([p, p], [y(r), y(r) + 0.12], color="#52514e", linewidth=1)
        ax.text(p, y(r) + 0.2, l, ha="center", va="bottom", fontsize=8.5, color="#52514e")
    ax.text(-4, y(r), label, ha="right", va="center", fontsize=10, color="#0b0b0b")

scale_row(0, "Points", np.arange(0, 101, 10), [str(v) for v in range(0, 101, 10)])
for i, (c, label, ticks) in enumerate(predictors, start=1):
    scale_row(i, label, [points(c, v) for v in ticks], [f"{v:g}" for v in ticks])
    ax.scatter(pt_points[c], y(i), s=60, color=PALETTE[1], zorder=3, edgecolor="#fcfcfb", linewidth=1.5)
    ax.plot([pt_points[c]] * 2, [y(i), y(0)], color=PALETTE[1], linewidth=0.8, alpha=0.5)
r_tot = len(predictors) + 1
to_x = lambda T: T / total_max * 100                     # total-points scale drawn across the full width
tot_ticks = np.arange(0, total_max + 1, 25)
scale_row(r_tot, "Total points", [to_x(t) for t in tot_ticks], [f"{t:g}" for t in tot_ticks])
probs = [p for p in [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9]
         if prob_of_total(0) <= p <= prob_of_total(total_max)]
T_of = lambda p: (np.log(p / (1 - p)) - base_lp) * scale
scale_row(r_tot + 1, "Risk of recurrence", [to_x(T_of(p)) for p in probs], [f"{p:.0%}" for p in probs])
ax.scatter(to_x(pt_total), y(r_tot), s=60, color=PALETTE[1], zorder=3, edgecolor="#fcfcfb", linewidth=1.5)
ax.scatter(to_x(pt_total), y(r_tot + 1), s=60, color=PALETTE[1], zorder=3, edgecolor="#fcfcfb", linewidth=1.5)
ax.plot([to_x(pt_total)] * 2, [y(r_tot), y(r_tot + 1)], color=PALETTE[1], linewidth=0.8)
ax.text(to_x(pt_total) + 1.5, y(r_tot + 1) - 0.35,
        f"Example patient: {pt_total:.0f} points → {prob_of_total(pt_total):.0%} risk",
        fontsize=9.5, color="#0b0b0b", va="top")
ax.set_xlim(-30, 104)
ax.set_ylim(y(r_tot + 1) - 0.8, y(0) + 0.6)
ax.set_title("Nomogram: 5-year recurrence risk  (orange = example patient: 62 y, 3 cm, 4 nodes, grade 3)",
             loc="left", fontsize=11.5)
fig.tight_layout()
