# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rows = [
    ("project", "data", "raw", 820), ("project", "data", "processed", 310),
    ("project", "models", "checkpoints", 540), ("project", "models", "exports", 120),
    ("project", "notebooks", "outputs", 95), ("project", "notebooks", "ipynb", 40),
    ("project", "src", "python", 12), ("project", "src", "tests", 6),
    ("project", "docs", "images", 55), ("project", "docs", "markdown", 3),
]
df = pd.DataFrame(rows, columns=["root", "folder", "sub", "size_mb"])
df.head()

# %% plot
fig = px.icicle(df, path=[px.Constant("project"), "folder", "sub"], values="size_mb", color="folder",
                color_discrete_sequence=PALETTE, title="Disk usage by folder (MB)")
fig.update_traces(root_color="#d0cfca", tiling=dict(orientation="v"),
                  marker=dict(line=dict(color="#fcfcfb", width=2)))
fig.update_layout(width=850, height=500, margin=dict(t=60, l=10, r=10, b=10))
