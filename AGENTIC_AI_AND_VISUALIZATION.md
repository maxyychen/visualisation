# Agentic AI and Data Visualization

*A memo on how AI agents are changing the way charts are made, what the research says about their
limits, and what that means for people who use this library. Status as of October 2026.*

**Agentic AI** here means LLM-based systems that do more than answer a question: they plan steps,
write and run code, inspect the result (including the rendered image), and iterate until the task
is done.

---

## Contents

1. [Summary](#1-summary)
2. [How the workflow changes](#2-how-the-workflow-changes)
3. [What the research says about the limits](#3-what-the-research-says-about-the-limits)
4. [What it means for practitioners](#4-what-it-means-for-practitioners)
5. [Lessons from building this library with agents](#5-lessons-from-building-this-library-with-agents)
6. [Checklist: using an AI agent to make a chart](#6-checklist-using-an-ai-agent-to-make-a-chart)
7. [Making this library agent-ready](#7-making-this-library-agent-ready)
8. [Sources](#8-sources)

---

## 1. Summary

- **Making charts is no longer the bottleneck; judging them is.** Anyone can now describe a chart
  in plain language and get working code in seconds. The scarce skills are choosing the right
  message, spotting misleading encodings and verifying the numbers.
- **Agents are capable but unreliable.** Benchmarks show uneven quality across chart types,
  frequent readability problems, and code that doesn't always match the output.
- **AI is a poor judge of charts.** Most vision-language models are fooled by misleading designs,
  so the agent that made a chart can't be trusted to review it alone.
- **Guardrails must be explicit and executable.** Rules, automated checks and unit tests turn agent
  output from plausible to trustworthy.

---

## 2. How the workflow changes

| Stage | Before | With agents |
|---|---|---|
| **Asking** | Learn a tool, choose a chart, write code | Describe the question in plain language ("natural language to visualization", NL2VIS) |
| **Preparing data** | Manual reshaping, filtering and joins | The agent writes the transformation code. Microsoft's *Data Formulator 2* (CHI 2025) delegates data transformation to AI while the user keeps visual control |
| **Generating** | One chart at a time | Multi-step pipelines that summarise the data, propose analysis goals, then generate, run and filter chart code (*LIDA*, ACL 2023; newer systems split this across several specialised agents) |
| **Iterating** | Edit code by hand | Conversational refinement ("sort it, highlight Q4, use a log scale"), with a history of earlier versions to return to |
| **Checking** | A person reviews it | The agent renders the chart, looks at the image and fixes collisions, clipping or wrong scales |
| **Explaining** | Write the commentary yourself | Auto-generated titles, captions, summaries and "how to read it" notes |
| **Scaling up** | One analyst, one chart | Many agents working in parallel on a catalogue, a report or a dashboard |

What stays the same: the reader. Perception, attention and the risk of being misled don't change
because a machine drew the chart.

---

## 3. What the research says about the limits

### Chart generation is uneven
- **VisEval** (IEEE VIS 2024 Best Paper) tested LLMs on 2,524 natural-language queries across 146
  databases, scoring validity, legality and readability with automated checkers. Every model
  struggled with some chart types, stacked bars especially. Extra information in the prompt didn't
  reliably help and sometimes hurt. Many charts that rendered were hard to read: overlapping text,
  poor scales.
- **A 2026 comparative survey of NL2VIS frameworks** found inconsistent performance across chart
  types and recurring problems such as unreliable library behaviour and weak alignment between the
  generated code and the rendered output. It concludes that progress depends more on
  well-orchestrated systems than on bigger models.
- **A 2026 EuroVis state-of-the-art report** (48 papers) maps LLM roles across the whole pipeline,
  from data querying to chart generation and explanation, and notes persistent weaknesses in
  spatial reasoning.

### AI is easily misled by charts
- **A 2025 study** analysed more than 16,000 responses from ten vision-language models on eight
  misleading chart designs and found that **most models are deceived**, even when the underlying
  data is identical.
- **Misleading ChartQA** (EMNLP 2025) provides 3,026 examples covering 21 types of misleading design
  across 10 chart types, a benchmark for this weakness.
- An **earlier 2024 study** with fewer designs and simpler prompts was more optimistic. The broader
  2025 results suggest the problem is real and not yet solved.

### Generated code is a security risk
Tools such as LIDA execute the code they generate and advise running them in a secure environment.
Treat agent-generated plotting code like any untrusted code: sandbox it, and never let it touch
production data or credentials.

---

## 4. What it means for practitioners

1. **Invest in judgement, not syntax.** Knowing *which* chart, *why*, and *when not to* matters more
   than knowing matplotlib's API. This library's *purpose / when to use / avoid when* notes, the
   [bad-vs-good family](README.md#15-bad-vs-good) and [How to Choose a Chart](HOW_TO_CHOOSE_A_CHART.md)
   are written for exactly this.
2. **State the message before you prompt.** "Show that our fund lost less than the index in 2022"
   gets a far better chart than "plot the fund data". Agents optimise for the request they're given.
3. **Make the rules executable.** A style guide that only people read is ignored by agents. Encode
   it as code: shared palettes, lint checks, validation scripts.
4. **Test the numbers, not just the picture.** A chart can look right while the statistic behind it
   is wrong. Unit tests on the calculations are the only reliable defence.
5. **Keep a human in the loop for decisions.** Use agents to draft, explore and iterate. Have a
   person approve anything that informs an investment, clinical or business decision.
6. **Expect more interactive and exploratory output.** Agents make what-if pages and linked
   dashboards cheap to produce, so the question shifts to whether interaction actually helps the
   reader.
7. **Protect sensitive data.** Prompts, generated notebooks and executed outputs can all contain
   the data you analysed. De-identify patient and client data, and check where your agent sends it.

---

## 5. Lessons from building this library with agents

Most of the library's 214 charts were written by AI agents working in parallel, each given a family
or a set of methods. This is what made that work, and what went wrong along the way.

### What made it reliable
- **Shared, explicit rules.** A categorical palette whose fixed order was checked for colour-vision
  deficiency (neighbouring colours stay distinguishable), and
  written anti-patterns (no dual axes, bars from zero, ≤ 8 hues), so agents drew consistent charts.
- **A single source of truth.** Each chart is a `meta.yaml` plus a `chart.py`, and a generator
  builds the scripts, notebooks, README and gallery. Agents edited sources; the build did the rest.
- **An executable check.** `build_library.py --check` runs every script, and the full build
  executes every notebook. A chart that doesn't run can't be merged.
- **Visual review of every preview.** Agents and a reviewer looked at rendered contact sheets and
  fixed label collisions, clipped text and misleading layouts that no automated check caught.
- **Unit tests for the statistics.** `vizlib.finance` and `vizlib.health` have 45 tests,
  including cross-checks against an established library (`lifelines`).
- **Verified citations.** Research methods cite papers found by search, not written from memory,
  and every DOI was checked against the DOI registry and Crossref (title, authors, year, pages).
  Where no DOI exists or none could be confirmed, the citation links to the paper's official page.

### What the safeguards caught
| Problem | Caught by |
|---|---|
| Months with no data shown as 0% returns in the monthly-returns table | Unit test |
| Deaths at exactly time 0 silently dropped from the Kaplan–Meier estimate | Cross-check against `lifelines` |
| A regression confidence band that changed on every rebuild (unseeded bootstrap) | Reproducibility check (byte-identical rebuilds) |
| Play buttons and sliders appearing in every frame of animated GIFs | Visual review |
| "How to read it" notes that described results the chart didn't show | Visual review |
| YAML list items silently read as dictionaries, crashing the README build | The build failing; a validation rule was added afterwards |
| Families that mixed unrelated topics ("Scientific & clinical", "Multivariate & ML") | Human review |
| Dozens of "how to read it" notes and titles that contradicted their own charts, plus wrong statistics: RECIST progression measured from baseline instead of the nadir, CONSORT totals that included patients lost to follow-up, a calibration example where the "over-confident" model wasn't | A second, independent review by agents that hadn't written the charts |

The pattern: **agents produced plausible work quickly; tests, builds, independent review and human
judgement made it correct.** The agents that wrote a chart were consistently worse at spotting its
errors than a fresh reviewer, which matches the research on AI judging charts. The last row is a reminder that some judgements (what belongs together, what a reader
needs) still came from a person.

---

## 6. Checklist: using an AI agent to make a chart

**Before you ask**
- [ ] Write the one-sentence message the chart must show
- [ ] Describe the data: columns, units, time range, how many rows
- [ ] State the audience and the medium (slide, report, dashboard)
- [ ] Remove or de-identify sensitive data

**When you ask**
- [ ] Ask for the chart family and why, not just the code
- [ ] Ask for a title that states the finding
- [ ] Give your style rules (palette, no dual axes, bars from zero), or point to this library's style

**Before you use it**
- [ ] Run the code yourself, in a sandbox
- [ ] Check key numbers against the source data
- [ ] Check the chart against [the common mistakes](HOW_TO_CHOOSE_A_CHART.md#common-mistakes-and-their-fixes)
- [ ] Run the five-second test on a colleague
- [ ] Confirm uncertainty is shown for estimates, forecasts and backtests

---

## 7. Making this library agent-ready

Proposed next steps, not yet built:

1. **Machine-readable catalogue** (`catalog.json`): every chart's purpose, when to use, when to
   avoid, data shape, level and code location, so an agent can look up the right chart instead of
   guessing.
2. **Chart linter** (`vizlib.lint`): automated checks for the bad-vs-good mistakes (dual axes,
   truncated bars, rainbow colour maps, too many colours, unsorted categories, missing labels)
   that an agent runs on its own output before showing it. This targets the weaknesses VisEval and
   the misleading-chart studies found.
3. **Chart recommender / agent tool:** `recommend(df, message)` profiles a DataFrame and returns
   ranked charts with their "avoid when" warnings, optionally packaged as an MCP tool or skill so
   coding agents can call it directly.

---

## 8. Sources

**Benchmarks and surveys**
- *VisEval: A benchmark for data visualization in the era of large language models* (Microsoft Research & ShanghaiTech University, 2024). IEEE VIS 2024 Best Paper; IEEE TVCG. <https://arxiv.org/abs/2407.00981> · [VIS listing](https://aa.ieeevis.org/year/2024/program/paper_v-full-1332.html)
- *Rethinking NL2VIS: A comparative survey of LLM-based natural-language-to-visualisation frameworks* (PAKDD 2026). <https://ink.library.smu.edu.sg/sis_research/11281>
- *State of the art of LLM-enabled interaction with visualization* (EuroVis 2026 STAR). <https://www.arxiv.org/abs/2601.14943>
- *Talk to your data: a survey on natural language interfaces for data visualization in the age of LLMs* (HKUST-GZ, 2025). <https://dsa.hkust-gz.edu.cn/blog/2025/06/09/talk-to-your-data-a-survey-on-natural-language-interfaces-for-data-visualization-in-the-age-of-llms/>
- *LLM-based data science agents: a survey of capabilities, challenges, and future directions* (2025). <https://arxiv.org/abs/2510.04023>

**Systems**
- *Data Formulator 2: Iterative creation of data visualizations, with AI transforming data along the way* (Microsoft Research). CHI 2025. <https://arxiv.org/abs/2408.16119> · [Microsoft Research](https://www.microsoft.com/en-us/research/publication/data-formulator-2-iteratively-creating-rich-visualizations-with-ai/)
- Dibia, V. (2023). LIDA: A tool for automatic generation of grammar-agnostic visualizations and infographics using large language models. ACL 2023 System Demonstrations, 113–126. <https://arxiv.org/abs/2303.02927>
- *CoDA*, a multi-agent visualization system (2025). <https://arxiv.org/abs/2510.03194>

**AI and misleading charts**
- *Vision-language models deceived by misleading chart designs* (2025; 16,000+ responses, ten models). <https://papers.cool/arxiv/2508.09716>
- Chen et al. (2025). Misleading ChartQA. EMNLP 2025. <https://arxiv.org/abs/2503.18172>
- Lo, L. Y.-H. & Qu, H. (2024). How good (or bad) are LLMs at detecting misleading visualizations? IEEE VIS 2024. <https://arxiv.org/abs/2407.17291>

*Summaries of the surveys and the 2025 misleading-chart study are based on their abstracts, and the VisEval findings on chart types and prompts come from a secondary summary of the paper. Author names are given only where the search results confirmed them.*
