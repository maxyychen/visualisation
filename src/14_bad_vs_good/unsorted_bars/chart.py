# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(4)
clinics = ["Cardiology", "Dermatology", "Endocrinology", "Gastroenterology", "Hematology",
           "Nephrology", "Neurology", "Oncology", "Orthopedics", "Pulmonology"]
df = pd.DataFrame({"clinic": clinics, "wait_min": rng.uniform(12, 45, len(clinics)).round(0)})
TARGET = 30
df

# %% plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Misleading: alphabetical, rainbow, rotated labels.
ax1.bar(df["clinic"], df["wait_min"], color=plt.get_cmap("rainbow")(np.linspace(0, 1, len(df))))
ax1.tick_params(axis="x", rotation=60)
ax1.set_ylabel("Average wait (min)")
ax1.set_title("✗ Misleading: alphabetical, rainbow, tilted labels", fontsize=11.5)

# Better: sorted, horizontal, one color + highlight for "over target".
d = df.sort_values("wait_min")
colors = np.where(d["wait_min"] > TARGET, PALETTE[1], GRAY)
ax2.barh(d["clinic"], d["wait_min"], color=colors, height=0.7)
ax2.axvline(TARGET, color="#52514e", linewidth=1)
ax2.text(TARGET + 0.5, -0.9, f"{TARGET}-min target", fontsize=9, color="#52514e", va="center")
ax2.set_ylim(-1.3, len(d) - 0.4)
for y, v in enumerate(d["wait_min"]):
    ax2.text(v + (1.6 if abs(v - TARGET) < 2 else 0.6), y, f"{v:.0f}", va="center", fontsize=9, color="#52514e")
ax2.set_xlabel("Average wait (min)")
ax2.set_xlim(0, d["wait_min"].max() * 1.15)
ax2.grid(axis="y", visible=False)
ax2.set_title("✓ Better: sorted, horizontal, color = over target", fontsize=11.5)
fig.tight_layout()
