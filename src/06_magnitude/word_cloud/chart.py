# %% setup
from vizlib.mpl_style import *  # noqa: F401,F403  (inlined on build)

# %% data
from collections import Counter
rng = np.random.default_rng(2)
vocab = {"easy": 40, "transfer": 34, "login": 30, "fast": 28, "fees": 26, "support": 24,
         "update": 22, "crash": 18, "secure": 16, "card": 15, "budget": 14, "savings": 12,
         "notifications": 11, "statement": 10, "investing": 9, "biometric": 8, "slow": 7,
         "exchange": 6, "interest": 6, "cashback": 5, "outage": 4, "verification": 4, "loan": 3}
freqs = {w: int(f * rng.uniform(0.8, 1.2)) for w, f in vocab.items()}
pd.Series(freqs).sort_values(ascending=False).head(10)

# %% plot
from wordcloud import WordCloud
blues = ["#104281", "#1c5cab", "#2a78d6", "#5598e7"]
wc = WordCloud(width=1000, height=500, background_color="#fcfcfb", prefer_horizontal=0.9,
               color_func=lambda *a, **k: blues[np.random.default_rng(len(a[0])).integers(4)],
               random_state=1).generate_from_frequencies(freqs)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), gridspec_kw={"width_ratios": [2, 1]})
ax1.imshow(wc, interpolation="bilinear")
ax1.axis("off")
ax1.set_title("Banking app reviews: most frequent words")
top = pd.Series(freqs).sort_values().tail(10)
ax2.barh(top.index, top.values, color=PALETTE[0], height=0.7)
ax2.set_title("Top 10 terms (precise)")
ax2.set_xlabel("Mentions")
ax2.grid(axis="y", visible=False)
fig.tight_layout()
