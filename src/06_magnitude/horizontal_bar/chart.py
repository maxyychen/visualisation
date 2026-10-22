# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
df = pd.DataFrame({
    "language": ["JavaScript", "Python", "SQL", "TypeScript", "Bash/Shell", "Java",
                 "C#", "C++", "Go", "Rust", "Kotlin", "R"],
    "pct": [62, 58, 51, 40, 33, 30, 27, 23, 14, 13, 9, 5],
}).sort_values("pct")
df.tail()

# %% plot
fig, ax = plt.subplots(figsize=(8, 5.5))
bars = ax.barh(df["language"], df["pct"], color=PALETTE[0], height=0.7)
ax.bar_label(bars, fmt="%d%%", padding=4, fontsize=9, color="#52514e")
ax.xaxis.set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.grid(False)
ax.set_title("Languages used by respondents (% of respondents)")
fig.tight_layout()

# %% alt:plotly
import plotly.express as px
fig = px.bar(df, x="pct", y="language", orientation="h", text="pct",
             color_discrete_sequence=PALETTE, title="Languages used by respondents (% of respondents)",
             labels={"pct": "% of respondents", "language": ""})
fig.update_traces(texttemplate="%{text}%", textposition="outside")
fig.update_layout(height=480)
fig.show()

# %% alt:altair
import altair as alt
base = alt.Chart(df).encode(y=alt.Y("language:N", sort="-x", title=None),
                            x=alt.X("pct:Q", title="% of respondents"))
chart = (base.mark_bar(color=PALETTE[0], cornerRadiusEnd=3)
         + base.mark_text(align="left", dx=4, color="#52514e").encode(text=alt.Text("pct:Q", format=".0f"))
         ).properties(title="Languages used by respondents (% of respondents)", width=460, height=340)
chart
