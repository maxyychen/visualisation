# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
from scipy import stats
rng = np.random.default_rng(1)
spend = rng.uniform(5, 50, 80)
sales = 120 + 6.2 * spend + rng.normal(0, 40, 80)
df = pd.DataFrame({"ad_spend_k": spend, "sales_k": sales})
x, y = "ad_spend_k", "sales_k"
labels = dict(x="Advertising spend ($k / week)", y="Sales ($k / week)", title="Sales rise with advertising spend")
fit = stats.linregress(df[x], df[y])
print(f"slope={fit.slope:.2f}  r={fit.rvalue:.2f}  p={fit.pvalue:.1e}")

# %% plot
import seaborn as sns
fig, ax = plt.subplots(figsize=(7.5, 5))
sns.regplot(data=df, x=x, y=y, ax=ax, ci=95, seed=0,
            scatter_kws=dict(s=30, alpha=0.6, color=PALETTE[0], edgecolor="#fcfcfb"),
            line_kws=dict(color=PALETTE[1], linewidth=2))
ax.text(0.03, 0.95, f"r = {fit.rvalue:.2f}\nn = {len(df)}", transform=ax.transAxes,
        va="top", fontsize=10, color="#52514e")
ax.set_xlabel(labels["x"])
ax.set_ylabel(labels["y"])
ax.set_title(labels["title"])
fig.tight_layout()

# %% real-data
from scipy import stats
import plotly.express as px
df = px.data.tips()
x, y = "total_bill", "tip"
labels = dict(x="Total bill ($)", y="Tip ($)",
              title="Tips rise with the size of the bill (244 restaurant bills)")
fit = stats.linregress(df[x], df[y])
print(f"slope={fit.slope:.2f}  r={fit.rvalue:.2f}  p={fit.pvalue:.1e}")

# %% alt:plotly
import plotly.express as px
fig = px.scatter(df, x=x, y=y, trendline="ols", opacity=0.65,
                 color_discrete_sequence=PALETTE, trendline_color_override=PALETTE[1],
                 labels={x: labels["x"], y: labels["y"]}, title=labels["title"])
fig.show()   # hover the line for the fitted equation and R²
