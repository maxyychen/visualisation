# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(5)
df = pd.DataFrame({"minutes": rng.gamma(4.5, 7, 2000) + 8})
df["minutes"].describe().round(1)

# %% plot
fig, ax = plt.subplots(figsize=(8, 4.8))
ax.hist(df["minutes"], bins=40, color=PALETTE[0], edgecolor="#fcfcfb", linewidth=0.8)
med = df["minutes"].median()
ax.axvline(med, color="#0b0b0b", linewidth=1.2)
ax.text(med + 1, ax.get_ylim()[1] * 0.92, f"median {med:.0f} min", fontsize=9)
ax.set_xlabel("Delivery time (minutes)")
ax.set_ylabel("Orders")
ax.set_title("Distribution of delivery times")
ax.grid(axis="x", visible=False)
fig.tight_layout()

# %% alt:plotly
import plotly.express as px
fig = px.histogram(df, x="minutes", nbins=40, color_discrete_sequence=PALETTE,
                   labels={"minutes": "Delivery time (minutes)"}, title="Distribution of delivery times")
fig.add_vline(x=df["minutes"].median(), line_color="#0b0b0b", line_width=1.2,
              annotation_text=f"median {df['minutes'].median():.0f} min")
fig.update_traces(marker_line_color="#fcfcfb", marker_line_width=0.8)
fig.update_layout(yaxis_title="Orders", bargap=0)
fig.show()

# %% alt:altair
import altair as alt
bars = alt.Chart(df).mark_bar(color=PALETTE[0]).encode(
    x=alt.X("minutes:Q", bin=alt.Bin(maxbins=40), title="Delivery time (minutes)"),
    y=alt.Y("count():Q", title="Orders"), tooltip=["count()"])
median = alt.Chart(df).mark_rule(color="#0b0b0b").encode(x="median(minutes):Q")
chart = (bars + median).properties(title="Distribution of delivery times", width=520, height=300)
chart
