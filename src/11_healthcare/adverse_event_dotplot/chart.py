# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(90)
n_trt = n_ctl = 250
events = {  # adverse event: (placebo incidence, true relative risk)
    "Nausea": (0.12, 2.4), "Neutropenia": (0.06, 3.0), "Rash": (0.08, 2.2), "Fatigue": (0.20, 1.35),
    "Diarrhoea": (0.10, 1.6), "Alopecia": (0.03, 2.5), "Decreased appetite": (0.07, 1.5),
    "Peripheral neuropathy": (0.04, 1.8), "Anaemia": (0.09, 1.3), "Vomiting": (0.06, 1.4),
    "Headache": (0.14, 1.05), "Constipation": (0.09, 1.1), "Insomnia": (0.07, 0.95),
    "Back pain": (0.08, 0.9), "Cough": (0.10, 1.0), "Dizziness": (0.06, 1.1),
    "Upper resp. infection": (0.11, 0.85), "Arthralgia": (0.07, 0.8), "Hypertension": (0.05, 0.75),
    "Pyrexia": (0.05, 1.2),
}
rows = []
for name, (p0, rr) in events.items():
    x_ctl = rng.binomial(n_ctl, p0)
    x_trt = rng.binomial(n_trt, min(p0 * rr, 0.95))
    a, b = x_trt + 0.5, x_ctl + 0.5                      # 0.5 added to every cell of the 2x2 table
    log_rr = np.log((a / (n_trt + 1)) / (b / (n_ctl + 1)))
    se = np.sqrt(1 / a - 1 / (n_trt + 1) + 1 / b - 1 / (n_ctl + 1))
    rows.append((name, x_trt / n_trt, x_ctl / n_ctl, np.exp(log_rr),
                 np.exp(log_rr - 1.96 * se), np.exp(log_rr + 1.96 * se)))
ae = (pd.DataFrame(rows, columns=["event", "inc_trt", "inc_ctl", "rr", "rr_lo", "rr_hi"])
      .sort_values("rr").reset_index(drop=True))
ae.tail()

# %% plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 7), sharey=True, width_ratios=[1, 1.15])
y = np.arange(len(ae))
signal = ae["rr_lo"] > 1
ax1.hlines(y, ae[["inc_trt", "inc_ctl"]].min(axis=1) * 100, ae[["inc_trt", "inc_ctl"]].max(axis=1) * 100,
           color="#d0cfca", linewidth=1.5)
ax1.scatter(ae["inc_ctl"] * 100, y, s=45, color=PALETTE[0], label="Placebo", zorder=3,
            edgecolor="#fcfcfb", linewidth=1.2)
ax1.scatter(ae["inc_trt"] * 100, y, s=45, color=PALETTE[1], label="Treatment", zorder=3,
            edgecolor="#fcfcfb", linewidth=1.2)
ax1.set_yticks(y, ae["event"])
for lab, s in zip(ax1.get_yticklabels(), signal):
    lab.set_fontweight("bold" if s else "normal")
ax1.set_xlabel("Patients with event (%)")
ax1.set_title("Incidence by arm", fontsize=11)
ax1.legend(loc="lower right", fontsize=9)
ax1.grid(axis="y", visible=False)

ax2.hlines(y, ae["rr_lo"], ae["rr_hi"], color=np.where(signal, "#52514e", "#b8b7b1"), linewidth=1.6)
ax2.scatter(ae["rr"], y, s=40, color=np.where(signal, "#0b0b0b", "#8f8e88"), zorder=3)
ax2.axvline(1, color="#52514e", linewidth=1)
ax2.set_xscale("log")
ticks = [0.25, 0.5, 1, 2, 4, 8]
ax2.set_xticks(ticks, [f"{t:g}" for t in ticks])
ax2.minorticks_off()
ax2.set_xlim(0.12, 12)
ax2.set_xlabel("Relative risk, treatment vs. placebo (95% CI, log scale)")
ax2.set_title("Relative risk", fontsize=11)
ax2.grid(axis="y", visible=False)
ax2.text(0.98, 0.02, "bold rows: CI entirely above 1", transform=ax2.transAxes, ha="right",
         va="bottom", fontsize=8.5, color="#52514e")
fig.suptitle("Adverse events: incidence and relative risk (simulated trial, 250 per arm)",
             x=0.02, ha="left", fontsize=13, fontweight="bold")
fig.tight_layout()
