# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
events = pd.DataFrame([
    ("2003-01-01", "matplotlib\nreleased"),
    ("2006-01-01", "NumPy 1.0"),
    ("2008-01-01", "pandas\nstarted"),
    ("2012-06-01", "seaborn\nfirst commit"),
    ("2013-01-01", "Bokeh\nannounced"),
    ("2014-12-01", "Jupyter\nspun off IPython"),
    ("2015-11-01", "plotly.js\nopen-sourced"),
    ("2016-09-01", "Altair\nreleased"),
    ("2019-07-01", "Panel / HoloViz"),
    ("2021-10-01", "Streamlit 1.0"),
], columns=["date", "event"])
events["date"] = pd.to_datetime(events["date"])
events

# %% plot
import matplotlib.dates as mdates
levels = np.tile([1.6, -1.6, 0.9, -0.9], len(events))[:len(events)]
fig, ax = plt.subplots(figsize=(11, 4.2))
ax.axhline(0, color="#52514e", linewidth=1.2)
ax.vlines(events["date"], 0, levels, color=GRAY, linewidth=1)
ax.scatter(events["date"], np.zeros(len(events)), s=50, color=PALETTE[0], zorder=3,
           edgecolor="#fcfcfb", linewidth=1.5)
for d, lvl, txt in zip(events["date"], levels, events["event"]):
    ax.text(d, lvl + (0.12 if lvl > 0 else -0.12), f"{txt}\n{d:%Y}" if lvl > 0 else f"{d:%Y}\n{txt}",
            ha="center", va="bottom" if lvl > 0 else "top", fontsize=8.5)
ax.set_ylim(-3, 3)
ax.yaxis.set_visible(False)
for s in ["left", "bottom"]:
    ax.spines[s].set_visible(False)
ax.grid(False)
ax.xaxis.set_major_locator(mdates.YearLocator(2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.set_title("Milestones in the Python data-viz ecosystem (approximate dates)")
fig.tight_layout()
