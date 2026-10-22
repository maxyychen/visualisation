# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(10)
classes = {"Compact": (1.4, 110, 1250, 42, 22), "SUV": (2.5, 200, 1900, 28, 45),
           "Sports": (3.5, 380, 1500, 22, 90)}
rows = []
for cls, (eng, hp, kg, mpg, price) in classes.items():
    for _ in range(20):
        rows.append([cls, eng * rng.normal(1, .12), hp * rng.normal(1, .12),
                     kg * rng.normal(1, .07), mpg * rng.normal(1, .1), price * rng.normal(1, .15)])
df = pd.DataFrame(rows, columns=["class", "Engine (L)", "Power (hp)", "Weight (kg)",
                                 "MPG", "Price ($k)"])
title = "Car classes across five specifications"
df.head()

# %% plot
cols = df.columns[1:]
norm = (df[cols] - df[cols].min()) / (df[cols].max() - df[cols].min())
fig, ax = plt.subplots(figsize=(10, 5))
for i, (cls, g) in enumerate(norm.groupby(df["class"])):
    for _, row in g.iterrows():
        ax.plot(range(len(cols)), row.values, color=PALETTE[i], alpha=0.45, linewidth=1)
    ax.plot([], [], color=PALETTE[i], label=cls, linewidth=2)
for j, c in enumerate(cols):
    ax.axvline(j, color="#8c8b86", linewidth=1)
    fmt = (lambda v: f"{v:,.0f}") if df[c].max() >= 100 else (lambda v: f"{v:.3g}")
    ax.text(j, 1.03, fmt(df[c].max()), ha="center", fontsize=8, color="#52514e")
    ax.text(j, -0.06, fmt(df[c].min()), ha="center", fontsize=8, color="#52514e")
ax.set_xticks(range(len(cols)), cols)
ax.set_yticks([])
ax.grid(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_visible(False)
ax.set_ylim(-0.1, 1.08)
ax.legend(loc="upper center", ncol=3, bbox_to_anchor=(0.5, -0.08))
ax.set_title(title)
fig.tight_layout()

# %% real-data
import plotly.express as px
iris = px.data.iris()
df = pd.DataFrame({"class": iris["species"],
                   "Sepal length (cm)": iris["sepal_length"], "Sepal width (cm)": iris["sepal_width"],
                   "Petal length (cm)": iris["petal_length"], "Petal width (cm)": iris["petal_width"]})
title = "Iris species across four measurements (Fisher, 1936)"
df.head()

# %% alt:plotly
import plotly.graph_objects as go
codes = df["class"].astype("category").cat.codes
names = list(df["class"].astype("category").cat.categories)
k = len(names)
scale = [[i / k, PALETTE[i]] for i in range(k)] + [[(i + 1) / k, PALETTE[i]] for i in range(k)]
fig = go.Figure(go.Parcoords(
    line=dict(color=codes, colorscale=sorted(scale), cmin=-0.5, cmax=k - 0.5),
    dimensions=[dict(label=c, values=df[c]) for c in df.columns[1:]]))
fig.update_layout(title=f"{title}  ·  colours: " + ", ".join(names), height=440)
fig.show()   # drag along an axis to filter (brushing)
