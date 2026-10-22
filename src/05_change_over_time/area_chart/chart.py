# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(4)
dates = pd.date_range("2024-01-01", periods=182, freq="D")
weekly = 1 + 0.25 * np.sin(2 * np.pi * dates.dayofweek / 7)
visits = (2000 + np.linspace(0, 1500, len(dates))) * weekly + rng.normal(0, 150, len(dates))
df = pd.DataFrame({"date": dates, "visits": visits.round()})
df.head()

# %% plot
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.fill_between(df["date"], df["visits"], color=PALETTE[0], alpha=0.25, linewidth=0)
ax.plot(df["date"], df["visits"], color=PALETTE[0], linewidth=1.5)
ax.set_ylim(0, None)
ax.set_ylabel("Visits per day")
ax.set_title("Daily website visits")
fig.tight_layout()

# %% alt:plotly
import plotly.express as px
fig = px.area(df, x="date", y="visits", color_discrete_sequence=PALETTE,
              labels={"date": "", "visits": "Visits per day"}, title="Daily website visits")
fig.update_traces(line_width=1.5)
fig.update_layout(hovermode="x unified")
fig.show()

# %% alt:altair
import altair as alt
chart = alt.Chart(df).mark_area(line={"color": PALETTE[0]}, color=PALETTE[0], opacity=0.35).encode(
    x=alt.X("date:T", title=None), y=alt.Y("visits:Q", title="Visits per day"),
    tooltip=["date:T", "visits:Q"],
).properties(title="Daily website visits", width=560, height=280)
chart
