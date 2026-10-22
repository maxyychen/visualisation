# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
nodes = ["Sign-ups", "Activated", "Browsed only", "Bounced",
         "Pro plan", "Basic plan", "Free tier", "Churned", "Win-back email"]
links = pd.DataFrame([
    ("Sign-ups", "Activated", 380), ("Sign-ups", "Browsed only", 520), ("Sign-ups", "Bounced", 100),
    ("Activated", "Pro plan", 210), ("Activated", "Basic plan", 150), ("Activated", "Free tier", 20),
    ("Browsed only", "Free tier", 140), ("Browsed only", "Churned", 380),
    ("Bounced", "Win-back email", 100),
], columns=["source", "target", "users"])
links

# %% plot
idx = {n: i for i, n in enumerate(nodes)}
node_colors = ["#52514e", PALETTE[1], PALETTE[0], PALETTE[3],
               "#b8b7b1", "#b8b7b1", "#b8b7b1", "#b8b7b1", "#b8b7b1"]
def rgba(hex_, a):
    h = hex_.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"
link_colors = [rgba(node_colors[idx[t]] if s == "Sign-ups" else node_colors[idx[s]], 0.45)
               for s, t in zip(links["source"], links["target"])]
fig = go.Figure(go.Sankey(
    node=dict(label=nodes, color=node_colors, pad=18, thickness=16,
              line=dict(color="#fcfcfb", width=1)),
    link=dict(source=links["source"].map(idx), target=links["target"].map(idx),
              value=links["users"], color=link_colors),
))
fig.update_layout(title="Customer journey from sign-up to plan (n = 1,000)",
                  width=900, height=520, margin=dict(t=60, l=20, r=20, b=20))
