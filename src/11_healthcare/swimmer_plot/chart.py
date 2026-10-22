# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(13)
n = 24
resp = rng.choice(["Complete response", "Partial response", "Stable disease", "Progressive disease"],
                  n, p=[0.12, 0.33, 0.33, 0.22])
base = {"Complete response": 22, "Partial response": 15, "Stable disease": 8, "Progressive disease": 3}
dur = np.array([max(1.0, rng.normal(base[r], base[r] * 0.35)) for r in resp]).round(1)
responder = np.isin(resp, ["Complete response", "Partial response"])
onset = np.where(responder, np.minimum(dur * 0.9, rng.uniform(1.5, 4, n)), np.nan).round(1)
ongoing = (rng.random(n) < 0.3) & (resp != "Progressive disease")   # best response PD means it progressed
progressed = ~ongoing & (resp != "Complete response")
df = pd.DataFrame({"patient": [f"P{i:02d}" for i in range(1, n + 1)], "months": dur,
                   "best_response": resp, "response_onset": onset,
                   "progressed": progressed, "ongoing": ongoing}).sort_values("months")
df.head()

# %% plot
colors = {"Complete response": "#104281", "Partial response": "#5598e7",
          "Stable disease": GRAY, "Progressive disease": PALETTE[1]}
fig, ax = plt.subplots(figsize=(9, 7))
y = np.arange(len(df))
ax.barh(y, df.months, color=df.best_response.map(colors), height=0.7)
ax.scatter(df.response_onset, y, marker="^", s=45, color="#0b0b0b", zorder=3, label="Response onset")
pr = df.progressed.values
ax.scatter(df.months[pr] + 0.35, y[pr], marker="x", s=40, color="#0b0b0b", zorder=3, label="Progression")
og = df.ongoing.values
ax.scatter(df.months[og] + 0.5, y[og], marker=">", s=45, color="#0b0b0b", zorder=3,
           label="Ongoing treatment")
ax.set_yticks(y, df.patient, fontsize=8)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Months on treatment")
ax.set_title("Treatment duration and response by patient")
from matplotlib.patches import Patch
handles = [Patch(color=c, label=k) for k, c in colors.items()]
h2, _ = ax.get_legend_handles_labels()
ax.legend(handles=handles + h2, loc="lower right", fontsize=8.5)
fig.tight_layout()
