# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)
from matplotlib.patches import FancyBboxPatch

# %% data
flow = {
    "assessed": 480,
    "excluded": {"Not meeting inclusion criteria": 72, "Declined to participate": 38, "Other reasons": 10},
    "arms": {
        "Intervention": {"allocated": 181, "received": 176, "not_received": 5,
                         "lost": {"Lost to follow-up": 7, "Discontinued intervention (adverse events)": 4}},
        "Control": {"allocated": 179, "received": 179, "not_received": 0,
                    "lost": {"Lost to follow-up": 9, "Discontinued intervention (withdrew consent)": 3}},
    },
}
randomised = flow["assessed"] - sum(flow["excluded"].values())
for a in flow["arms"].values():  # patients who discontinued are still followed; only those lost lack outcome data
    a["no_outcome"] = a["lost"]["Lost to follow-up"]
    a["analysed"] = a["allocated"] - a["no_outcome"]
    assert a["received"] + a["not_received"] == a["allocated"]
assert randomised == sum(a["allocated"] for a in flow["arms"].values())
print("randomised:", randomised)

# %% plot
fig, ax = plt.subplots(figsize=(10, 9.5))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.grid(False)

def box(x, y, w, h, text, main=True, bold=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.3,rounding_size=1",
                                facecolor="#fcfcfb" if main else "#f3f2ef",
                                edgecolor=PALETTE[0] if main else "#b8b7b1", linewidth=1.4))
    ax.text(x, y, text, ha="center", va="center", fontsize=9, color="#0b0b0b",
            fontweight="bold" if bold else "normal", linespacing=1.4)

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#52514e", linewidth=1.1, shrinkA=0, shrinkB=0))

def stage(y, label):
    ax.add_patch(FancyBboxPatch((0.5, y - 2), 13, 4, boxstyle="round,pad=0.2,rounding_size=1",
                                facecolor="#cde2fb", edgecolor="none"))
    ax.text(7, y, label, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#0d366b")

box(57, 94, 30, 6, f"Assessed for eligibility\n(n = {flow['assessed']})", bold=True)
excl = "\n".join(f"• {k} (n = {v})" for k, v in flow["excluded"].items())
box(82, 82, 32, 12, f"Excluded (n = {sum(flow['excluded'].values())})\n{excl}", main=False)
ax.plot([57, 57], [91, 82], color="#52514e", linewidth=1.1)
arrow(57, 82, 66, 82)
arrow(57, 82, 57, 72)
box(57, 69, 24, 6, f"Randomised (n = {randomised})", bold=True)
stage(69, "Enrolment")
for x, (arm, a) in zip([36, 78], flow["arms"].items()):
    ax.plot([57, 57, x, x], [66, 61, 61, 59], color="#52514e", linewidth=1.1)
    arrow(x, 59.5, x, 58)
    nr = f"\n• Did not receive (n = {a['not_received']})" if a["not_received"] else "\n• Did not receive (n = 0)"
    box(x, 52, 37, 11, f"Allocated to {arm.lower()} (n = {a['allocated']})\n"
                       f"• Received allocated intervention (n = {a['received']}){nr}")
    lost = "\n".join(f"• {k} (n = {v})" for k, v in a["lost"].items())
    arrow(x, 46.5, x, 38)
    box(x, 32, 37, 11, f"Follow-up\n{lost}", main=False)
    arrow(x, 26.5, x, 18)
    box(x, 12, 37, 11, f"Analysed (n = {a['analysed']})\n• Excluded from analysis: no primary\n  outcome data (n = {a['no_outcome']})")
stage(52, "Allocation")
stage(32, "Follow-up")
stage(12, "Analysis")
ax.text(0.5, 99.5, "CONSORT 2010 flow diagram", fontsize=13, fontweight="bold", va="top")
fig.tight_layout()
