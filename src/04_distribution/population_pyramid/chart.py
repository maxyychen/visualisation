# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
bands = [f"{a}–{a + 4}" for a in range(0, 90, 5)] + ["90+"]
age_mid = np.arange(2.5, 95, 5)
base = np.exp(-((age_mid - 48) / 30) ** 2) * 4 + 1.2
base[-4:] *= np.array([0.8, 0.55, 0.3, 0.12])
male = base * (1.02 - age_mid / 400)
female = base * (0.98 + age_mid / 500)
tot = male.sum() + female.sum()
df = pd.DataFrame({"band": bands, "male": male / tot * 100, "female": female / tot * 100})
df.round(2).tail()

# %% plot
fig, ax = plt.subplots(figsize=(8, 6.5))
ax.barh(df["band"], -df["male"], color=PALETTE[0], height=0.85, label="Male")
ax.barh(df["band"], df["female"], color=PALETTE[1], height=0.85, label="Female")
ax.axvline(0, color="#fcfcfb", linewidth=2)
lim = 4.5
ticks = np.arange(-4, 5, 1)
ax.set_xticks(ticks, [f"{abs(t)}%" for t in ticks])
ax.set_xlim(-lim, lim)
ax.set_xlabel("Share of total population")
ax.set_title("Population pyramid")
ax.grid(axis="y", visible=False)
ax.legend(loc="upper right")
fig.tight_layout()
