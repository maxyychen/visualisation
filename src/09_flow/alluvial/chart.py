# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(21)
n = 1500
age = rng.choice(["18–34", "35–54", "55+"], n, p=[0.35, 0.4, 0.25])
p_channel = {"18–34": [0.65, 0.25, 0.10], "35–54": [0.45, 0.35, 0.20], "55+": [0.2, 0.35, 0.45]}
channel = np.array([rng.choice(["App", "Web", "Phone"], p=p_channel[a]) for a in age])
p_sat = {"App": [0.6, 0.3, 0.1], "Web": [0.45, 0.4, 0.15], "Phone": [0.35, 0.35, 0.3]}
sat = np.array([rng.choice(["Satisfied", "Neutral", "Unsatisfied"], p=p_sat[c]) for c in channel])
df = pd.DataFrame({"Age": age, "Channel": channel, "Satisfaction": sat})
df.value_counts().head(8)

# %% plot
color_idx = df["Channel"].map({"App": 0, "Web": 1, "Phone": 2})
fig = go.Figure(go.Parcats(
    dimensions=[
        dict(label="Age", values=df["Age"], categoryorder="array",
             categoryarray=["18–34", "35–54", "55+"]),
        dict(label="Channel", values=df["Channel"], categoryorder="array",
             categoryarray=["App", "Web", "Phone"]),
        dict(label="Satisfaction", values=df["Satisfaction"], categoryorder="array",
             categoryarray=["Satisfied", "Neutral", "Unsatisfied"]),
    ],
    line=dict(color=color_idx, colorscale=[[0, PALETTE[0]], [0.5, PALETTE[1]], [1, PALETTE[2]]],
              shape="hspline"),
    hoveron="color", arrangement="freeform",
))
fig.update_layout(title="Customer journey: age → channel → satisfaction (n = 1,500)",
                  width=900, height=520, margin=dict(t=70, l=60, r=60, b=30))
