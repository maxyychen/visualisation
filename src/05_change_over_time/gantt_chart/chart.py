# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
tasks = pd.DataFrame([
    ("Requirements", "Plan", "2025-01-06", 14, 1.0),
    ("Architecture", "Plan", "2025-01-20", 14, 1.0),
    ("Backend API", "Build", "2025-02-03", 42, 0.8),
    ("Frontend UI", "Build", "2025-02-17", 49, 0.6),
    ("Data migration", "Build", "2025-03-10", 21, 0.3),
    ("Integration test", "Test", "2025-03-31", 21, 0.0),
    ("User acceptance", "Test", "2025-04-21", 14, 0.0),
    ("Launch", "Test", "2025-05-05", 5, 0.0),
], columns=["task", "phase", "start", "days", "done"])
tasks["start"] = pd.to_datetime(tasks["start"])
tasks["end"] = tasks["start"] + pd.to_timedelta(tasks["days"], unit="D")
tasks

# %% plot
import matplotlib.dates as mdates
phase_color = {"Plan": PALETTE[0], "Build": PALETTE[1], "Test": PALETTE[2]}
today = pd.Timestamp("2025-03-24")
fig, ax = plt.subplots(figsize=(10, 4.5))
for i, r in tasks.iterrows():
    c = phase_color[r["phase"]]
    ax.barh(i, r["days"], left=r["start"], color=c, alpha=0.3, height=0.6)
    ax.barh(i, r["days"] * r["done"], left=r["start"], color=c, height=0.6)
ax.axvline(today, color="#e34948", linewidth=1.5)
ax.text(today, -0.8, " today", color="#e34948", va="bottom")
ax.set_yticks(range(len(tasks)), tasks["task"])
ax.invert_yaxis()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.grid(axis="y", visible=False)
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in phase_color.values()]
ax.legend(handles, phase_color.keys(), loc="lower left", ncol=3)
ax.set_title("Project schedule (solid = completed)")
fig.tight_layout()
