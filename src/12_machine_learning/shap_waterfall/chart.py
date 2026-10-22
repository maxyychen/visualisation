# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from sklearn.linear_model import LogisticRegression

# %% data
rng = np.random.default_rng(5)
n = 5000
X = pd.DataFrame({
    "Credit utilisation (%)": rng.uniform(0, 100, n),
    "Debt-to-income (%)": rng.normal(30, 10, n).clip(0, 80),
    "Delinquencies (2 yrs)": rng.poisson(0.3, n),
    "Income ($k)": rng.lognormal(np.log(65), 0.4, n),
    "Account age (yrs)": rng.gamma(3, 3, n),
    "Credit inquiries (6 mo)": rng.poisson(1.2, n),
    "Loan amount ($k)": rng.lognormal(np.log(18), 0.5, n),
    "Employment (yrs)": rng.gamma(2, 3, n),
})
beta_true = np.array([0.035, 0.04, 0.6, -0.012, -0.08, 0.25, 0.012, -0.05])
logit = -3.0 + (X - X.mean()).to_numpy() @ beta_true
default = rng.binomial(1, 1 / (1 + np.exp(-logit)))
model = LogisticRegression(C=1e6, max_iter=5000).fit(X, default)

applicant = pd.Series({"Credit utilisation (%)": 82, "Debt-to-income (%)": 41, "Delinquencies (2 yrs)": 1,
                       "Income ($k)": 110, "Account age (yrs)": 3, "Credit inquiries (6 mo)": 4,
                       "Loan amount ($k)": 35, "Employment (yrs)": 14})
# Exact SHAP values for a linear model with independent features: beta_j * (x_j - E[x_j]), in log-odds.
shap = pd.Series(model.coef_[0] * (applicant - X.mean()).to_numpy(), index=X.columns)
base = model.intercept_[0] + model.coef_[0] @ X.mean().to_numpy()
pd.DataFrame({"value": applicant, "SHAP (log-odds)": shap.round(3)}).sort_values("SHAP (log-odds)")

# %% plot
sigmoid = lambda z: 1 / (1 + np.exp(-z))
fmt = {"Credit utilisation (%)": "{:.0f}%", "Debt-to-income (%)": "{:.0f}%", "Income ($k)": "${:.0f}k",
       "Loan amount ($k)": "${:.0f}k"}
order = shap.abs().sort_values(ascending=False).index
top, rest = order[:6], order[6:]
rows = [(f"{f.split(' (')[0]} = {fmt.get(f, '{:g}').format(applicant[f])}", shap[f]) for f in top]
rows.append((f"{len(rest)} other features", shap[rest].sum()))

fig, ax = plt.subplots(figsize=(9, 5.2))
start = base
for i, (label, v) in enumerate(rows):
    color = PALETTE[1] if v > 0 else PALETTE[0]
    ax.barh(i, v, left=start, height=0.62, color=color)
    ax.text(start + v + (0.03 if v > 0 else -0.03), i, f"{v:+.2f}", va="center",
            ha="left" if v > 0 else "right", fontsize=9, color="#52514e")
    if i < len(rows) - 1:
        ax.plot([start + v] * 2, [i + 0.31, i + 0.69], color="#8f8e88", linewidth=0.8)
    start += v
ax.set_yticks(range(len(rows)), [r[0] for r in rows])
ax.invert_yaxis()
for x in (base, start):
    ax.axvline(x, color="#8f8e88", linewidth=0.8)
ax.text(base, -0.75, f"Average applicant: {base:.2f} log-odds (PD {sigmoid(base):.1%})",
        ha="center", va="bottom", fontsize=9, color="#52514e")
ax.text(start, len(rows) - 0.3, f"This applicant: {start:.2f} log-odds (PD {sigmoid(start):.1%})",
        ha="center", va="top", fontsize=9, color="#0b0b0b", fontweight="bold")
ax.set_ylim(len(rows) + 0.1, -1.2)
ax.set_xlabel("Model output (log-odds of default)  ·  orange raises risk, blue lowers it")
ax.set_title("Why this applicant scored high risk")
ax.grid(axis="y", visible=False)
fig.tight_layout()
