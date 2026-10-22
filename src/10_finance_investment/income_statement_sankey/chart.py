# %% setup
from vizlib.plotly_style import *  # noqa: F401,F403  (inlined on build)

# %% data
links = pd.DataFrame([
    ("Products", "Revenue", 62), ("Services", "Revenue", 38),
    ("Revenue", "Gross profit", 58), ("Revenue", "Cost of revenue", 42),
    ("Gross profit", "Operating profit", 24), ("Gross profit", "R&D", 14),
    ("Gross profit", "Sales & marketing", 13), ("Gross profit", "G&A", 7),
    ("Operating profit", "Net income", 18), ("Operating profit", "Income tax", 5),
    ("Operating profit", "Interest", 1),
], columns=["source", "target", "value_bn"])
links

# %% plot
nodes = list(dict.fromkeys(links["source"].tolist() + links["target"].tolist()))
profit = {"Gross profit", "Operating profit", "Net income"}
cost = {"Cost of revenue", "R&D", "Sales & marketing", "G&A", "Income tax", "Interest"}


def rgba(hex_color, alpha):
    h = hex_color.lstrip("#")
    return f"rgba({int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}, {alpha})"


def node_color(n, alpha=1.0):
    return rgba(PALETTE[0] if n in profit else PALETTE[1] if n in cost else "#7a7974", alpha)


inflow = links.groupby("target")["value_bn"].sum()
outflow = links.groupby("source")["value_bn"].sum()
totals = {n: max(inflow.get(n, 0), outflow.get(n, 0)) for n in nodes}
idx = {n: i for i, n in enumerate(nodes)}
stage_x = {"Products": 0.01, "Services": 0.01, "Revenue": 0.24, "Gross profit": 0.48, "Cost of revenue": 0.48,
           "Operating profit": 0.72, "R&D": 0.72, "Sales & marketing": 0.72, "G&A": 0.72,
           "Net income": 0.99, "Income tax": 0.99, "Interest": 0.99}
stage_y = {"Products": 0.3, "Services": 0.8, "Revenue": 0.5, "Cost of revenue": 0.22, "Gross profit": 0.7,
           "R&D": 0.3, "Sales & marketing": 0.47, "G&A": 0.6, "Operating profit": 0.86,
           "Net income": 0.84, "Income tax": 0.95, "Interest": 0.99}   # costs above, profit along the bottom
fig = go.Figure(go.Sankey(
    arrangement="fixed",
    node=dict(label=[f"{n}  ${totals[n]:.0f}bn" for n in nodes], color=[node_color(n) for n in nodes],
              x=[stage_x[n] for n in nodes], y=[stage_y[n] for n in nodes],
              pad=18, thickness=16, line=dict(width=0)),
    link=dict(source=links["source"].map(idx), target=links["target"].map(idx), value=links["value_bn"],
              color=[node_color(t, 0.35) for t in links["target"]],
              hovertemplate="%{source.label} → %{target.label}<extra></extra>"),
))
fig.update_layout(title="Where the revenue goes: FY2025 income statement (illustrative, $bn)",
                  height=540, margin=dict(l=20, r=20, t=60, b=20), font_size=12)
