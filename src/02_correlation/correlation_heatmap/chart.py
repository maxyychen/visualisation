# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(10)
n = 180  # months
equity, rates, infl = rng.normal(0, 1, (3, n))  # common risk factors
assets = {
    "US equities":   0.9 * equity + 0.3 * rng.normal(size=n),
    "Intl equities": 0.8 * equity + 0.5 * rng.normal(size=n),
    "EM equities":   0.7 * equity + 0.7 * rng.normal(size=n),
    "REITs":         0.6 * equity - 0.3 * rates + 0.6 * rng.normal(size=n),
    "High yield":    0.5 * equity - 0.2 * rates + 0.6 * rng.normal(size=n),
    "US Treasuries": -0.3 * equity - 0.9 * rates + 0.3 * rng.normal(size=n),
    "Gold":          -0.1 * equity + 0.5 * infl + 0.8 * rng.normal(size=n),
    "Commodities":   0.3 * equity + 0.7 * infl + 0.6 * rng.normal(size=n),
}
df = pd.DataFrame(assets)
title = "Correlation of monthly returns across asset classes"
corr = df.corr().round(2)
corr

# %% plot
import seaborn as sns
mask = np.triu(np.ones_like(corr, dtype=bool))
# drop the all-masked first row / last column of the lower triangle
tri, tri_mask = corr.iloc[1:, :-1], mask[1:, :-1]
fig, ax = plt.subplots(figsize=(7.5, 6.2))
sns.heatmap(tri, mask=tri_mask, cmap=DIV_CMAP, vmin=-1, vmax=1, center=0, annot=True,
            fmt=".2f", annot_kws=dict(size=9), linewidths=2, linecolor="#fcfcfb",
            square=True, cbar_kws=dict(shrink=0.75, label="Pearson r"), ax=ax)
ax.grid(False)
ax.set_title(title)
fig.tight_layout()

# %% real-data
import plotly.express as px
prices = px.data.stocks().set_index("date")
df = prices.pct_change().dropna()          # weekly returns
df.columns = [c.upper() for c in df.columns]
title = "Correlation of weekly returns, six tech stocks (2018-2019)"
corr = df.corr().round(2)
corr

# %% alt:plotly
import plotly.express as px
lower = corr.where(np.tril(np.ones(corr.shape, dtype=bool), k=-1))
fig = px.imshow(lower, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                aspect="equal", title=title)
fig.update_layout(coloraxis_colorbar_title="Pearson r", height=560,
                  xaxis_showgrid=False, yaxis_showgrid=False)
fig.show()
