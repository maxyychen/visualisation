# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(17)
change = np.clip(rng.normal(-18, 32, 40), -100, 75).round(1)
change[rng.choice(40, 2, replace=False)] = -100
bor = np.select([change <= -100, change <= -30, change >= 20],
                ["Complete response", "Partial response", "Progressive disease"], "Stable disease")
df = pd.DataFrame({"patient": range(1, 41), "best_change": change, "response": bor})
df = df.sort_values("best_change", ascending=False).reset_index(drop=True)
df.response.value_counts()

# %% plot
colors = {"Progressive disease": PALETTE[1], "Stable disease": GRAY,
          "Partial response": "#5598e7", "Complete response": "#104281"}
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df.index, df.best_change, color=df.response.map(colors), width=0.8)
for v, lab in [(20, "+20%\nprogression"), (-30, "−30%\npartial response")]:
    ax.axhline(v, color="#52514e", linewidth=0.8)
    ax.text(1.01, v, lab, transform=ax.get_yaxis_transform(), va="center", fontsize=8, color="#52514e")
ax.axhline(0, color="#52514e", linewidth=1)
ax.set_xticks([]); ax.set_xlim(-0.8, len(df) - 0.2)
ax.grid(axis="x", visible=False)
ax.set_ylim(-105, 85)
ax.set_ylabel("Best change from baseline (%)"); ax.set_xlabel("Patients")
orr = df.response.isin(["Complete response", "Partial response"]).mean()
ax.set_title(f"Best tumour response (objective response rate {orr:.0%})")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c, label=k) for k, c in colors.items()], loc="upper right", fontsize=8.5)
fig.tight_layout()
