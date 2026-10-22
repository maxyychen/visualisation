# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
rng = np.random.default_rng(5)
chrom_len = np.array([249, 242, 198, 190, 181, 171, 159, 145, 138, 134, 135,
                      133, 114, 107, 102, 90, 83, 80, 59, 64, 47, 51])  # Mb
n_snp = (chrom_len / chrom_len.sum() * 40000).astype(int)
chrom = np.repeat(np.arange(1, 23), n_snp)
pos = np.concatenate([np.sort(rng.uniform(0, L, k)) for L, k in zip(chrom_len, n_snp)])
nlp = -np.log10(rng.uniform(size=len(chrom)))
for c, center, height in [(2, 120, 14), (6, 32, 22), (16, 54, 9.5)]:
    m = chrom == c
    nlp[m] += height * np.exp(-((pos[m] - center) / 0.8) ** 2) * rng.uniform(0.6, 1, m.sum())
df = pd.DataFrame({"chrom": chrom, "pos_mb": pos, "nlp": nlp})
offsets = np.r_[0, np.cumsum(chrom_len)[:-1]]
df["x"] = df.pos_mb + offsets[df.chrom - 1]
df.head()

# %% plot
gw, sug = -np.log10(5e-8), -np.log10(1e-5)
fig, ax = plt.subplots(figsize=(12, 5))
shades = [PALETTE[0], "#104281"]
for c, d in df.groupby("chrom"):
    ax.scatter(d.x, d.nlp, s=4, color=shades[c % 2], linewidth=0)
hit = df[df.nlp > gw]
ax.scatter(hit.x, hit.nlp, s=12, color=PALETTE[1], linewidth=0, label="Genome-wide significant")
ax.axhline(gw, color=PALETTE[1], linewidth=1)
ax.axhline(sug, color=GRAY, linewidth=1)
ax.text(df.x.max(), gw + 0.3, "p = 5×10⁻⁸", ha="right", fontsize=8, color="#52514e")
ax.text(df.x.max(), sug + 0.3, "p = 1×10⁻⁵", ha="right", fontsize=8, color="#52514e")
centers = df.groupby("chrom").x.median()
ax.set_xticks(centers, [str(c) if c < 18 or c % 2 == 0 else "" for c in centers.index])
ax.set_xlim(0, df.x.max() + 10); ax.set_ylim(0, df.nlp.max() + 2)
ax.grid(axis="x", visible=False)
ax.set_xlabel("Chromosome"); ax.set_ylabel("−log10 p")
ax.set_title("Genome-wide association scan (synthetic)")
ax.legend(loc="upper right")
fig.tight_layout()
