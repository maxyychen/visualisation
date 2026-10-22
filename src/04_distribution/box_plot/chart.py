# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(6)
segments = {"Card on file": (1.0, 0.5), "Small business": (2.9, 0.35), "Retail chain": (3.3, 0.3),
            "Enterprise": (3.6, 0.35), "Distributor": (3.5, 0.5), "Government": (3.9, 0.55)}
df = pd.concat([pd.DataFrame({"segment": d, "days_to_pay": rng.lognormal(mu, sd, 170)})
                for d, (mu, sd) in segments.items()], ignore_index=True)
order = df.groupby("segment")["days_to_pay"].median().sort_values().index.tolist()
df.groupby("segment")["days_to_pay"].median().round(1)

# %% plot
import seaborn as sns
fig, ax = plt.subplots(figsize=(8.5, 5))
sns.boxplot(data=df, x="segment", y="days_to_pay", order=order, color=PALETTE[0], width=0.55,
            boxprops=dict(alpha=0.35), linewidth=1.2,
            flierprops=dict(marker="o", markersize=3, markerfacecolor="#52514e",
                            markeredgecolor="none", alpha=0.5),
            medianprops=dict(color="#0b0b0b", linewidth=2), ax=ax)
ax.set_yscale("log")
ax.set_yticks([1, 2, 5, 10, 30, 60, 120, 240], ["1", "2", "5", "10", "30", "60", "120", "240"])
ax.set_xlabel(None)
ax.set_ylabel("Days to pay (log scale)")
ax.set_title("Days to pay an invoice, by customer segment")
ax.grid(axis="x", visible=False)
fig.tight_layout()

# %% alt:plotly
import plotly.express as px
fig = px.box(df, x="segment", y="days_to_pay", points="outliers", log_y=True,
             category_orders={"segment": order}, color_discrete_sequence=PALETTE,
             labels={"segment": "", "days_to_pay": "Days to pay (log scale)"},
             title="Days to pay an invoice, by customer segment")
fig.show()   # hover a box for median, quartiles and fences
