# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
quarters = ["Q1", "Q2", "Q3", "Q4"]
df = pd.DataFrame({
    "Direct sales": [3200, 3500, 3350, 3800],
    "Partners":     [5400, 5600, 5900, 6100],
    "Online":       [1200, 1500, 1900, 2300],
}, index=quarters)
df

# %% plot
fig, ax = plt.subplots(figsize=(8, 5))
bottom = np.zeros(len(df))
for i, col in enumerate(df.columns):
    ax.bar(df.index, df[col], bottom=bottom, color=PALETTE[i], label=col,
           width=0.6, edgecolor="#fcfcfb", linewidth=2)
    bottom += df[col].values
for x, total in enumerate(bottom):
    ax.text(x, total + 150, f"${total / 1000:.1f}M", ha="center", fontsize=9, color="#52514e")
ax.set_ylabel("Revenue ($k)")
ax.set_title("Revenue by quarter and sales channel")
ax.grid(axis="x", visible=False)
ax.set_ylim(0, bottom.max() * 1.12)
ax.legend(ncol=3, loc="upper left")
fig.tight_layout()

# %% alt:plotly
import plotly.express as px
long = df.rename_axis("quarter").reset_index().melt(id_vars="quarter", var_name="channel", value_name="revenue")
fig = px.bar(long, x="quarter", y="revenue", color="channel", color_discrete_sequence=PALETTE,
             labels={"quarter": "", "revenue": "Revenue ($k)", "channel": ""},
             title="Revenue by quarter and sales channel")
fig.update_traces(marker_line_color="#fcfcfb", marker_line_width=2)
fig.show()

# %% alt:altair
import altair as alt
long = df.rename_axis("quarter").reset_index().melt(id_vars="quarter", var_name="channel", value_name="revenue")
chart = alt.Chart(long).mark_bar(stroke="#fcfcfb", strokeWidth=2).encode(
    x=alt.X("quarter:N", title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("revenue:Q", title="Revenue ($k)"),
    color=alt.Color("channel:N", sort=list(df.columns), title=None),
    order=alt.Order("stack:Q"), tooltip=["quarter", "channel", "revenue"],
).transform_calculate(stack=f"indexof({list(df.columns)}, datum.channel)"
).properties(title="Revenue by quarter and sales channel", width=380, height=320)
chart
