# How to Choose a Chart

A step-by-step guide for turning data into the right visualization. It applies the ideas in
[PRINCIPLES.md](PRINCIPLES.md) (why charts work or fail) as a working procedure (what to do, in
what order). Every chart named here links to a worked example in this library: a notebook with its
purpose, when to use it, when to avoid it, and runnable code.

**Short version:** know who will act on the chart, write the one thing they should notice, decide
whether it needs a chart at all, pick the family that matches the message and the data, choose the
simplest and most accurately read form in that family, draw it honestly, then test it on someone.

The steps fall into three phases. Each phase depends on the one before it: you can't pick a chart
family without a message, and you can't judge an encoding without a chart.

| Phase | Steps | Output |
|---|---|---|
| **A. Decide what to say** | 1–3 | One sentence, one audience, and a format (sentence, number, table or chart) |
| **B. Choose the chart** | 4–6 | A specific chart type |
| **C. Draw it well** | 7–9 | A finished, honest, tested chart |

---

## Contents

**A. Decide what to say**
1. [Know the audience and the decision](#step-1-know-the-audience-and-the-decision)
2. [Write the message as one sentence](#step-2-write-the-message-as-one-sentence)
3. [Decide whether you need a chart](#step-3-decide-whether-you-need-a-chart)

**B. Choose the chart**

4. [Name the relationship](#step-4-name-the-relationship)
5. [Fit the chart to your data](#step-5-fit-the-chart-to-your-data)
6. [Pick the simplest form that reads accurately](#step-6-pick-the-simplest-form-that-reads-accurately)

**C. Draw it well**

7. [Encode honestly](#step-7-encode-honestly)
8. [Design for the message](#step-8-design-for-the-message)
9. [Test it](#step-9-test-it)

**Reference**
- [Quick decision path](#quick-decision-path)
- [Finance and investment quick reference](#finance-and-investment-quick-reference)
- [Common mistakes and their fixes](#common-mistakes-and-their-fixes)
- [Pre-publication checklist](#pre-publication-checklist)
- [Using the library to choose](#using-the-library-to-choose)

---

# A. Decide what to say

## Step 1: Know the audience and the decision

A chart is chosen for a reader, not for a dataset. Before looking at the data, answer three
questions, ideally with the person who asked for the chart:

| Question | Why it matters | Example |
|---|---|---|
| **Who** will read it? | Sets how much context and chart literacy you can assume (step 6) | Investment committee vs. clients |
| **What** should they decide or do? | Tells you which comparison matters, and which **levers** they can pull | Rebalance, hold, or change manager |
| **How** will success be judged? | A correct chart of the wrong metric still leads to the wrong decision | Risk-adjusted return, not raw return |

Requesters assume you share their context. Ask what they want answered, what they expect to find,
and why it's needed now. If different readers have different perspectives (for example, risk vs.
sales), they may need different charts of the same data.

---

## Step 2: Write the message as one sentence

Finish the sentence **"The reader should see that…"**. The sentence is the specification for
everything that follows: its verb picks the chart family (step 4) and its subject is what you will
highlight (step 8).

| Sentence | What it tells you |
|---|---|
| "…our fund fell less than the index in 2022." | Change over time, against a benchmark |
| "…three clients make up 60% of revenue." | Part-to-whole, with the top items emphasised |
| "…daily returns have fatter tails than a normal distribution." | A distribution, compared with a reference |
| "…revenue rises with advertising spend." | A relationship between two numbers |

A good sentence compares the number to something (a target, a peer or the past). A number with no
comparison has no meaning, so if your sentence lacks one, add it now.

**You can't write the sentence yet?** Then you are **exploring**, not presenting. That is a separate
activity with different rules: make many quick, rough plots (a [histogram](04_distribution/histogram/histogram.ipynb), a
[pair plot](02_correlation/pair_plot/pair_plot.ipynb), a [line chart](05_change_over_time/line_chart/line_chart.ipynb), a [correlation heatmap](02_correlation/correlation_heatmap/correlation_heatmap.ipynb)),
polish nothing, and come back to this step once you know the message.

> **Rule:** one chart, one message. If you have two messages, make two charts.

---

## Step 3: Decide whether you need a chart

A chart earns its place only when the message is a **pattern**: a trend, a ranking, a spread, a
relationship. Otherwise a simpler format says it faster.

| The message is… | Use |
|---|---|
| One or two values | A sentence, or one big number: a [KPI stat tile](06_magnitude/kpi_stat_tile/kpi_stat_tile.ipynb), optionally with a [sparkline](05_change_over_time/sparklines/sparklines.ipynb) for context |
| Exact values the reader will look up | A table, or a [highlight table](06_magnitude/highlight_table/highlight_table.ipynb) when outliers matter |
| A trend, pattern or comparison | A chart: continue to step 4 |

A one-bar chart or a two-slice pie only adds ink. Likewise, if your chart would show very few
values in a large area, a sentence or a table would do better.

**One chart or a dashboard?** A single focused chart proves one point and supports a decision. A
dashboard gives an overview for monitoring, but it dilutes focus and lets a good metric hide a bad
one. If you have a message from step 2, make a chart.

---

# B. Choose the chart

## Step 4: Name the relationship

The verb in your sentence picks a chart **family**. These families follow the Financial Times
*Visual Vocabulary*, plus uncertainty. Within each row, **"Start with"** is the default that most
readers decode accurately; move to an alternative only when it answers the question better.

| The sentence is about… | Family | Start with | Then consider |
|---|---|---|---|
| A trend over time | Change over time | [Line chart](05_change_over_time/line_chart/line_chart.ipynb) | [Indexed line](05_change_over_time/indexed_line/indexed_line.ipynb), [small multiples](05_change_over_time/small_multiples_line/small_multiples_line.ipynb), [column](06_magnitude/column_chart/column_chart.ipynb) (few discrete periods) |
| A size comparison | Magnitude | [Bar chart](06_magnitude/horizontal_bar/horizontal_bar.ipynb) | [Grouped bar](06_magnitude/grouped_bar/grouped_bar.ipynb), [dumbbell](06_magnitude/dumbbell/dumbbell.ipynb), [bullet chart](06_magnitude/bullet_chart/bullet_chart.ipynb) (against a target) |
| Order (who's first, who's last) | Ranking | [Sorted bar](03_ranking/ordered_bar/ordered_bar.ipynb) | [Dot plot](03_ranking/cleveland_dot/cleveland_dot.ipynb), [lollipop](03_ranking/lollipop_ranking/lollipop_ranking.ipynb), [slope chart](03_ranking/slope_chart/slope_chart.ipynb), [bump chart](03_ranking/bump_chart/bump_chart.ipynb) (rank changes) |
| A difference from a baseline (target, zero, average) | Deviation | [Diverging bar](01_deviation/diverging_bar/diverging_bar.ipynb) | [Lollipop from mean](01_deviation/deviation_lollipop/deviation_lollipop.ipynb), [surplus/deficit line](01_deviation/surplus_deficit_line/surplus_deficit_line.ipynb) |
| A share of a total | Part-to-whole | [Stacked bar](07_part_to_whole/stacked_bar/stacked_bar.ipynb) (few parts) | [100% stacked bar](07_part_to_whole/percent_stacked_bar/percent_stacked_bar.ipynb), [waffle](07_part_to_whole/waffle_chart/waffle_chart.ipynb), [treemap](07_part_to_whole/treemap/treemap.ipynb) (many parts), [waterfall](07_part_to_whole/waterfall_chart/waterfall_chart.ipynb) (how a total changed) |
| Spread, skew, outliers | Distribution | [Histogram](04_distribution/histogram/histogram.ipynb) | [Box plot](04_distribution/box_plot/box_plot.ipynb), [violin](04_distribution/violin_plot/violin_plot.ipynb), [ECDF](04_distribution/ecdf/ecdf.ipynb) |
| Two or more variables moving together | Correlation | [Scatter](02_correlation/scatter/scatter.ipynb) | [Scatter + regression](02_correlation/scatter_regression/scatter_regression.ipynb), [bubble](02_correlation/bubble/bubble.ipynb), [correlation heatmap](02_correlation/correlation_heatmap/correlation_heatmap.ipynb) |
| Movement between stages or places | Flow | [Sankey](09_flow/sankey/sankey.ipynb) | [Funnel](09_flow/funnel_chart/funnel_chart.ipynb) (one path), [chord](09_flow/chord_diagram/chord_diagram.ipynb), [flow map](08_spatial/flow_map/flow_map.ipynb) |
| A location or geographic pattern | Spatial | [Choropleth](08_spatial/choropleth_world/choropleth_world.ipynb) (rates, not totals) | [Bubble map](08_spatial/bubble_map/bubble_map.ipynb) (counts), [tile grid map](08_spatial/tile_grid_map/tile_grid_map.ipynb), [hex-grid map](08_spatial/hexgrid_map/hexgrid_map.ipynb), [surprise map](08_spatial/surprise_map/surprise_map.ipynb) (counts that just follow population) |
| An estimate, forecast or risk | Uncertainty | [Points + confidence interval](12_scientific/error_bar_ci/error_bar_ci.ipynb), or a [fan chart](05_change_over_time/fan_chart/fan_chart.ipynb) for forecasts | [Gradient interval](14_uncertainty/gradient_interval/gradient_interval.ipynb), [quantile dot plot](14_uncertainty/quantile_dotplot/quantile_dotplot.ipynb), see [step 7](#show-uncertainty) |

Use a map only when **geography is the point**. If the message is "which region is highest", a
sorted bar answers it more accurately than a map.

---

## Step 5: Fit the chart to your data

The family says what kind of chart; the data decides which charts in that family are possible.

### Variable types → chart forms

| You have | Natural forms |
|---|---|
| 1 numeric variable | [Histogram](04_distribution/histogram/histogram.ipynb), [box plot](04_distribution/box_plot/box_plot.ipynb), [ECDF](04_distribution/ecdf/ecdf.ipynb) |
| 1 category + 1 number | [Sorted bar](03_ranking/ordered_bar/ordered_bar.ipynb), [dot plot](03_ranking/cleveland_dot/cleveland_dot.ipynb), [lollipop](03_ranking/lollipop_ranking/lollipop_ranking.ipynb) |
| 1 category + many observations per group | [Box plot](04_distribution/box_plot/box_plot.ipynb), [violin](04_distribution/violin_plot/violin_plot.ipynb), [strip/jitter](04_distribution/strip_jitter/strip_jitter.ipynb), [ridgeline](04_distribution/ridgeline/ridgeline.ipynb) |
| 2 categories + 1 number | [Grouped bar](06_magnitude/grouped_bar/grouped_bar.ipynb), [highlight table](06_magnitude/highlight_table/highlight_table.ipynb), [heatmap](09_flow/origin_destination_matrix/origin_destination_matrix.ipynb) |
| 2 numbers | [Scatter](02_correlation/scatter/scatter.ipynb), [hexbin](02_correlation/hexbin/hexbin.ipynb) (many points) |
| 3+ numbers | [Bubble](02_correlation/bubble/bubble.ipynb), [pair plot](02_correlation/pair_plot/pair_plot.ipynb), [parallel coordinates](06_magnitude/parallel_coordinates/parallel_coordinates.ipynb), [PCA biplot](02_correlation/pca_biplot/pca_biplot.ipynb) |
| Time + 1 number | [Line](05_change_over_time/line_chart/line_chart.ipynb), [column](06_magnitude/column_chart/column_chart.ipynb) (discrete periods), [calendar heatmap](05_change_over_time/calendar_heatmap/calendar_heatmap.ipynb) (daily) |
| Time + several numbers | [Line + highlight](05_change_over_time/line_highlight/line_highlight.ipynb), [small multiples](05_change_over_time/small_multiples_line/small_multiples_line.ipynb), [stacked area](05_change_over_time/stacked_area/stacked_area.ipynb) (only when the total is the message) |
| Parent → child hierarchy | [Treemap](07_part_to_whole/treemap/treemap.ipynb), [sunburst](07_part_to_whole/sunburst/sunburst.ipynb), [icicle](07_part_to_whole/icicle/icicle.ipynb) |
| From → to with amounts | [Sankey](09_flow/sankey/sankey.ipynb), [chord](09_flow/chord_diagram/chord_diagram.ipynb), [origin–destination matrix](09_flow/origin_destination_matrix/origin_destination_matrix.ipynb) |
| Nodes and links | [Network graph](09_flow/network_graph/network_graph.ipynb), [adjacency matrix](09_flow/adjacency_matrix/adjacency_matrix.ipynb) (large networks) |
| Overlapping sets | [Venn](07_part_to_whole/venn_diagram/venn_diagram.ipynb) (≤ 3 sets), [UpSet](12_scientific/upset_plot/upset_plot.ipynb) (more) |
| Locations | [Choropleth](08_spatial/choropleth_world/choropleth_world.ipynb) (regions), [bubble map](08_spatial/bubble_map/bubble_map.ipynb) (points), [hex-grid map](08_spatial/hexgrid_map/hexgrid_map.ipynb) (dense points) |
| Prices or returns | [Cumulative return vs. benchmark](10_finance_investment/cumulative_return_benchmark/cumulative_return_benchmark.ipynb), [drawdown](10_finance_investment/drawdown_underwater/drawdown_underwater.ipynb), [tear sheet](10_finance_investment/performance_tear_sheet/performance_tear_sheet.ipynb) |

Two rules follow from the data type:

- **Never join categories with a line.** A line implies continuity, so use it only for an ordered,
  continuous axis such as time.
- **A histogram is not a bar chart.** Its bars touch because the bins are continuous, and its
  conclusion can change with the bin width, so try several.

### How many things? (the scale check)

Most chart failures are scale failures. A chart that works for five items can fail for fifty.

| When you have… | The problem | Fix |
|---|---|---|
| More than ~10 categories | Bars become hard to scan | Sort, show top-N, fold the rest into "Other", or use a table |
| More than ~4 lines | Spaghetti | [Highlight one, grey the rest](05_change_over_time/line_highlight/line_highlight.ipynb), or [small multiples](05_change_over_time/small_multiples_line/small_multiples_line.ipynb) |
| More than ~6 colours needed | Hues become indistinguishable | Fold into "Other", facet into small multiples, or label directly |
| More than ~10,000 points | Overplotting turns into a blob | Transparency → [hexbin](02_correlation/hexbin/hexbin.ipynb) → [datashader](16_interactive_advanced/datashader_scatter/datashader_scatter.ipynb) |
| Millions of points in a line | Plotting libraries slow down; naive thinning drops spikes | [LTTB / MinMaxLTTB downsampling](16_interactive_advanced/lttb_downsampling/lttb_downsampling.ipynb) |
| Measures on different scales | The temptation of a dual axis | [Index to 100](05_change_over_time/indexed_line/indexed_line.ipynb), or stacked panels sharing the x-axis ([rolling metrics](10_finance_investment/rolling_metrics/rolling_metrics.ipynb)) |

### Check the data before you trust the picture

A well-drawn chart of misleading data is still misleading. Before committing to a chart, confirm:

- **The denominator is right.** Compare regions per capita, money over time after inflation, and
  both sides of a comparison on the same base. A totals map mostly shows where people live.
- **The comparison is fair.** Same time window, same interval lengths, same benchmark. Two data
  points can tell any story; a longer window shows whether the change is unusual.
- **Subgroups agree with the total.** A trend can reverse when groups are combined (Simpson's
  paradox), so plot subgroups before concluding from the aggregate.
- **The sample size is known**, and the sample isn't biased by how it was selected or who dropped out.
- **A correlation is not presented as a cause** unless you can rule out reverse causation and a
  hidden third variable.

See [PRINCIPLES.md §7](PRINCIPLES.md#7-statistical-traps) for each trap in detail.

---

## Step 6: Pick the simplest form that reads accurately

Steps 4 and 5 usually leave a few candidates. Choose between them with three questions, in this order.

### 1. Perceptual accuracy

Readers judge some visual properties far more accurately than others. From most to least accurate:

**position on a common scale → position on unaligned scales → length → angle → area → volume → colour**

Prefer the candidate whose key comparison sits highest on that list, and that asks the reader to do
as few kinds of judgement as possible. In practice this means redesigning *up* the ranking:

| Instead of | Use | Because |
|---|---|---|
| Pie or donut | Sorted bar or dot plot | Angle and area → length or position |
| Stacked bar (comparing inner segments) | Grouped bar or grouped dots | Every value gets a shared baseline |
| Two lines, when the gap is the message | One line of the difference | Readers misjudge the vertical gap between curves |
| Shaded map | Bars or a bubble map per region | Colour → length or position |
| Bubble size for the key variable | Put the key variable on an axis | Area is read poorly; keep size for the least important variable |
| 3D bars or pies | The same chart in 2D | Perspective distorts size |

A pie is acceptable only for two or three simple shares. Radar charts, circular bars and word
clouds rank poorly on every criterion; use a bar or dot plot instead.

### 2. The audience's chart literacy

Among accurate candidates, pick the simplest one this audience (step 1) can read without help.

| Audience | Prefer | Avoid |
|---|---|---|
| Executives, clients, board | **Basic** charts (bar, line, stat tile); one message each | Dense multi-panel charts, unexplained jargon |
| Analysts, investment committee | **Intermediate** charts (small multiples, heatmaps, distributions, intervals) | Oversimplification that hides risk |
| Specialists, research | **Advanced** charts ([HRP dendrogram](10_finance_investment/hrp_dendrogram/hrp_dendrogram.ipynb), [regime shading](10_finance_investment/regime_shading/regime_shading.ipynb), [event study](10_finance_investment/event_study/event_study.ipynb)) | Using them on a general audience without a how-to-read note |

An unfamiliar chart can be the right choice if it is the only one that shows the pattern, but then
it needs an annotation explaining how to read it.

### 3. The medium: static, interactive or animated?

| Choose | When | Library examples |
|---|---|---|
| **Static** (the default) | Reports, slides, print, decisions: anything that must say one thing reliably | Almost everything |
| **Interactive** | Readers need *their own* what-if, or their own slice of a large dataset | [Option payoff explorer](16_interactive_advanced/option_payoff_explorer/option_payoff_explorer.ipynb), [linked price & returns](16_interactive_advanced/linked_price_returns/linked_price_returns.ipynb), [crossfilter dashboard](16_interactive_advanced/crossfilter_dashboard/crossfilter_dashboard.ipynb) |
| **Animated** | The motion itself is the story (a curve inverting, a ranking reshuffling), usually in a presentation | [Animated yield curve](16_interactive_advanced/animated_yield_curve/animated_yield_curve.ipynb), [bar-chart race](16_interactive_advanced/bar_chart_race/bar_chart_race.ipynb) |

To **compare** across time, [small multiples beat animation](15_bad_vs_good/animation_vs_small_multiples/animation_vs_small_multiples.ipynb),
because animation makes readers remember earlier frames. Every interactive chart should also work as
a static image of its default state.

---

# C. Draw it well

## Step 7: Encode honestly

Visual size must be proportional to the value it represents. Each rule below prevents a specific
way a correct dataset turns into a false impression.

### Baselines and scales

The zero rule depends on what the reader decodes:

| Mark | Reader decodes | Zero baseline |
|---|---|---|
| Bar, column, lollipop | Length | **Required** ([see why](15_bad_vs_good/truncated_bar_axis/truncated_bar_axis.ipynb)) |
| Area, density | Area | **Required** |
| Line, dot, scatter | Position | **Optional**: choose a range that neither flattens a real trend nor exaggerates noise; if zero is nearby, include it |

- If you must break a bar axis, make the break obvious on the axis and on every broken bar.
- **Use a log scale for long-run growth** (prices, wealth, GDP) so that equal percentage moves look
  equal, and label it as log.
- **Size encodes area, not radius.** A bubble twice the value has twice the area ([see why](15_bad_vs_good/bubble_radius_scaling/bubble_radius_scaling.ipynb)).
  Never scale icons in both width and height for one-dimensional data.
- **Avoid dual y-axes.** The two ranges are arbitrary, so any crossing or slope can be manufactured
  ([see why](15_bad_vs_good/dual_axis_vs_indexed/dual_axis_vs_indexed.ipynb)). Index to a common
  start or use two panels. If a dual axis is unavoidable, colour-match each series to its axis.
- **Don't add dimensions the data lacks:** no 3D, no perspective, no decorative area.
- **Aspect ratio is an editorial choice.** The same line looks calm when wide and dramatic when tall.
  Start near 1:1.6 for time series and aim for average slopes near 45°.

### Show uncertainty

If a number is an **estimate, forecast, backtest or sample**, show its range. A single solid line
claims more certainty than you have. Draw forecasts dashed or lighter than actuals, and always state
what an interval shows (standard deviation, standard error, confidence interval or min–max).

| Situation | Chart |
|---|---|
| Group means or effects | [Points + 95% CI](12_scientific/error_bar_ci/error_bar_ci.ipynb), not a bar of means ([see why](15_bad_vs_good/dynamite_plot/dynamite_plot.ipynb)); [estimation plot](12_scientific/estimation_plot/estimation_plot.ipynb) to show the effect size itself |
| A forecast | [Fan chart](05_change_over_time/fan_chart/fan_chart.ipynb), [Monte Carlo wealth paths](10_finance_investment/monte_carlo_wealth/monte_carlo_wealth.ipynb) |
| Several estimates, compared | [Forest plot](12_scientific/forest_plot/forest_plot.ipynb), [gradient interval](14_uncertainty/gradient_interval/gradient_interval.ipynb), [half-eye plot](14_uncertainty/half_eye/half_eye.ipynb) |
| Risk for a non-technical audience | [Icon array](14_uncertainty/icon_array/icon_array.ipynb) ("7 in 100"), [quantile dot plot](14_uncertainty/quantile_dotplot/quantile_dotplot.ipynb) |
| Tail risk | [Return distribution with VaR/CVaR](10_finance_investment/return_distribution_var/return_distribution_var.ipynb) |
| Many simulated paths or curves | [Functional boxplot](14_uncertainty/functional_boxplot/functional_boxplot.ipynb): median path, central region and outlier paths |
| A result that depends on analyst choices | [Specification curve](14_uncertainty/specification_curve/specification_curve.ipynb): every reasonable specification at once |
| Repeated experiments (replicates) | [SuperPlot](12_scientific/superplot/superplot.ipynb): statistics on replicates, not on every point |
| A map of estimates with different precision | [Value-suppressing uncertainty palette](08_spatial/vsup_map/vsup_map.ipynb) |
| "Is this pattern real or noise?" | [Lineup protocol](12_scientific/lineup_protocol/lineup_protocol.ipynb): hide the real chart among null charts |

---

## Step 8: Design for the message

An honest chart can still bury its point. The goal now is to make the sentence from step 2 the first
thing the reader sees. Start from a bare chart and **add back only what helps**.

### Title the finding

Many readers see only the title, so it should carry the conclusion. "Fund beat the index in 4 of 5
down years" helps more than "Annual returns 2019–2024". Put context (units, period, source) in the
subtitle.

### Use colour for a job

"It looks nice" is not a job. Decide what colour does before picking any:

| Job | Rule | Example |
|---|---|---|
| **Emphasis** (this one matters) | One accent colour, everything else grey. The usual default. | [Line highlight](05_change_over_time/line_highlight/line_highlight.ipynb), [sorted bar](03_ranking/ordered_bar/ordered_bar.ipynb) |
| **Identity** (which series) | Distinct hues in a fixed order, about 6 at most; the same entity keeps the same colour in every chart | [Line chart](05_change_over_time/line_chart/line_chart.ipynb) |
| **Magnitude** (how much) | One hue, light = low, dark = high | [Highlight table](06_magnitude/highlight_table/highlight_table.ipynb), [choropleth](08_spatial/choropleth_world/choropleth_world.ipynb) |
| **Polarity** (above/below, gain/loss) | Two opposite hues around a neutral midpoint | [Monthly returns heatmap](10_finance_investment/monthly_returns_heatmap/monthly_returns_heatmap.ipynb) |

- Never use a rainbow colour map ([see why](15_bad_vs_good/rainbow_colormap/rainbow_colormap.ipynb)). It invents boundaries and fails for colour-blind readers.
- Don't rely on red/green alone for gains and losses. Blue/orange is colour-blind-safe; add signs (+/−) or labels too.
- Don't put the most important variable on colour. Colour is the least accurate channel.

### Label directly and declutter

- **Label directly** (at line ends, beside bars) instead of making readers decode a legend. Labels
  may share their series' colour; values and axis text stay in neutral ink.
- **Label selectively:** the endpoint, the maximum, the one that matters. Not a number on every point.
- **Sort categories** by value unless they have a natural order such as time, age bands or ratings ([see why](15_bad_vs_good/unsorted_bars/unsorted_bars.ipynb)).
- State units once, abbreviate large numbers ($18M), keep text horizontal.
- Use light gridlines or none; no 3D effects, shadows, heavy borders or background fills.

### Annotate the why

The chart shows *what* happened; an annotation explains *why*. Mark events, shade periods, show the
change so readers don't have to calculate it ("+2.1% YoY"), and draw a dashed target or benchmark
line when the message is a comparison against one. Annotate only what matters: a cluster of labels
makes an area look important.

---

## Step 9: Test it

**The five-second test:** show the chart to someone for five seconds, then ask "what did you see?"
If the answer isn't your sentence from step 2, fix it in this order, from cheapest to most drastic:

1. Move the message into the title.
2. Grey everything except what matters.
3. Remove series or categories that don't serve the message.
4. Sort the bars; replace the legend with direct labels.
5. Pick a different chart from the same family (step 4).
6. Still not working? Go back to step 2: the message may not be what the data actually shows.

Also check it at its final size (slide, page, phone) and in grayscale.

---

# Reference

## Quick decision path

A compressed version of steps 3–6. Each answer is a starting point, not a rule.

```
Is the story one or two numbers?       → sentence or KPI stat tile (+ sparkline)
Do readers need exact values?          → table / highlight table
Is it about change over time?
    ≤ 4 series                         → line chart
    one series matters                 → line + highlight (others grey)
    many series                        → small multiples
    different units/scales             → indexed line (= 100 at start)
    few discrete periods               → column chart
    the total over time is the point   → stacked area
Comparing categories?
    one measure                        → sorted bar / dot plot
    two time points                    → dumbbell or slope chart
    two measures per category          → grouped bar
    against a target or zero           → bullet chart / diverging bar
Shares of a total?
    few parts                          → stacked bar or waffle
    many parts or a hierarchy          → treemap / sunburst
    how a total got from A to B        → waterfall
Shape of values?
    one group                          → histogram
    several groups                     → box / violin / ridgeline
    comparing percentiles              → ECDF
Relationship between numbers?
    two numbers                        → scatter (+ trend line)
    > 10k points                       → hexbin → datashader
    many variables                     → correlation heatmap / pair plot
Movement between stages or places?     → funnel (one path) / sankey (branches) / flow map
Where? (geography is the point)        → choropleth of rates / bubble map of counts
Risk, estimates or forecasts?          → points + CI / fan chart / VaR distribution
```

---

## Finance and investment quick reference

| Question | Chart |
|---|---|
| How did the fund do vs. its benchmark? | [Cumulative return vs. benchmark](10_finance_investment/cumulative_return_benchmark/cumulative_return_benchmark.ipynb) (log scale), [annual returns](10_finance_investment/annual_returns_bar/annual_returns_bar.ipynb) |
| How bad did it get, and how long to recover? | [Drawdown (underwater)](10_finance_investment/drawdown_underwater/drawdown_underwater.ipynb) |
| Is performance consistent month to month? | [Monthly returns heatmap](10_finance_investment/monthly_returns_heatmap/monthly_returns_heatmap.ipynb) |
| Everything on one page | [Performance tear sheet](10_finance_investment/performance_tear_sheet/performance_tear_sheet.ipynb) (`python -m vizlib.finance prices.csv …`) |
| Is risk stable over time? | [Rolling metrics](10_finance_investment/rolling_metrics/rolling_metrics.ipynb), [rolling beta](10_finance_investment/rolling_beta_ci/rolling_beta_ci.ipynb), [rolling correlation](10_finance_investment/rolling_correlation/rolling_correlation.ipynb) |
| How big are the tails? | [Return distribution with VaR/CVaR](10_finance_investment/return_distribution_var/return_distribution_var.ipynb), [tail dependence](10_finance_investment/tail_dependence/tail_dependence.ipynb) |
| Where does portfolio risk come from? | [Risk contribution](10_finance_investment/risk_contribution/risk_contribution.ipynb), [factor exposure](10_finance_investment/factor_exposure/factor_exposure.ipynb), [stress-test tornado](10_finance_investment/stress_test_tornado/stress_test_tornado.ipynb) |
| Is the allocation efficient? | [Efficient frontier](10_finance_investment/efficient_frontier/efficient_frontier.ipynb), [risk/return scatter](10_finance_investment/risk_return_scatter/risk_return_scatter.ipynb) |
| Why did we beat (or miss) the benchmark? | [Brinson attribution](10_finance_investment/brinson_attribution/brinson_attribution.ipynb) |
| How do assets cluster? | [Correlation heatmap](02_correlation/correlation_heatmap/correlation_heatmap.ipynb), [correlation network](10_finance_investment/correlation_network_mst/correlation_network_mst.ipynb), [TMFG network](10_finance_investment/tmfg_network/tmfg_network.ipynb), [HRP dendrogram](10_finance_investment/hrp_dendrogram/hrp_dendrogram.ipynb) |
| Is a fund's outperformance skill or luck? | [Funnel plot](12_scientific/funnel_plot/funnel_plot.ipynb) (alpha vs. track-record length) |
| Is my backtest robust? | [Specification curve](14_uncertainty/specification_curve/specification_curve.ipynb) |
| Are the model's default probabilities reliable? | [CORP reliability diagram](13_machine_learning/corp_reliability_diagram/corp_reliability_diagram.ipynb) |
| Which of two forecasts is better? | [Murphy diagram](13_machine_learning/murphy_diagram/murphy_diagram.ipynb) |
| Why did the model score this applicant high-risk? | [SHAP waterfall](13_machine_learning/shap_waterfall/shap_waterfall.ipynb) |
| What is the market doing? | [Candlestick + moving averages](10_finance_investment/candlestick_ma_volume/candlestick_ma_volume.ipynb), [sector heatmap](10_finance_investment/sector_heatmap/sector_heatmap.ipynb), [market breadth](10_finance_investment/market_breadth/market_breadth.ipynb) |
| What are rates telling us? | [Yield curve](10_finance_investment/yield_curve/yield_curve.ipynb), [yield curve history](10_finance_investment/yield_curve_history/yield_curve_history.ipynb), [animated yield curve](16_interactive_advanced/animated_yield_curve/animated_yield_curve.ipynb) |
| What does this option position do? | [Option payoff](10_finance_investment/option_payoff/option_payoff.ipynb), [option payoff explorer](16_interactive_advanced/option_payoff_explorer/option_payoff_explorer.ipynb) (interactive) |
| What is the company worth? | [Football field](10_finance_investment/football_field_valuation/football_field_valuation.ipynb), [DCF sensitivity table](10_finance_investment/dcf_sensitivity_table/dcf_sensitivity_table.ipynb), [DCF explorer](16_interactive_advanced/dcf_explorer/dcf_explorer.ipynb) |
| Where does the revenue go, and why did it change? | [Income statement sankey](10_finance_investment/income_statement_sankey/income_statement_sankey.ipynb), [revenue bridge](10_finance_investment/revenue_bridge/revenue_bridge.ipynb), [waterfall](07_part_to_whole/waterfall_chart/waterfall_chart.ipynb) |
| Will the money last? | [Monte Carlo wealth](10_finance_investment/monte_carlo_wealth/monte_carlo_wealth.ipynb), [retirement planner](16_interactive_advanced/retirement_planner/retirement_planner.ipynb) (interactive) |
| Lump sum or dollar-cost averaging? | [Compounding & DCA](10_finance_investment/compounding_dca/compounding_dca.ipynb) |

Finance-specific rules (applications of step 5 and step 7):
- Compare performance against a benchmark, net of fees, over the **same** period.
- Show **risk next to return**, never return alone.
- Use log scales for long histories and **index** series to a common start (= 100) when comparing.
- Pick the start date honestly; a cherry-picked start date is the most common way performance charts mislead.
- Adjust long-horizon money for inflation, and mark simulated or backtested results as such.

---

## Common mistakes and their fixes

Each links to a side-by-side example in the **Bad vs. good** family.

| Mistake | Step | Why it misleads | Fix |
|---|---|---|---|
| [Pie with close values](15_bad_vs_good/pie_close_values/pie_close_values.ipynb) | 6 | Angles can't be compared | Sorted bar |
| [Spaghetti lines](15_bad_vs_good/spaghetti_vs_highlight/spaghetti_vs_highlight.ipynb) | 5 | Nothing stands out | Highlight one, grey the rest |
| [Overplotting](15_bad_vs_good/overplotting/overplotting.ipynb) | 5 | Density is invisible | Transparency, hexbin, datashader |
| [Animation for comparison](15_bad_vs_good/animation_vs_small_multiples/animation_vs_small_multiples.ipynb) | 6 | Relies on memory | Small multiples |
| [Truncated bar axis](15_bad_vs_good/truncated_bar_axis/truncated_bar_axis.ipynb) | 7 | Small differences look huge | Start bars at zero, or use dots |
| [Dual y-axis](15_bad_vs_good/dual_axis_vs_indexed/dual_axis_vs_indexed.ipynb) | 7 | Axis ranges are arbitrary, so crossings and slopes are invented | Index to 100, or two panels |
| [Bubbles scaled by radius](15_bad_vs_good/bubble_radius_scaling/bubble_radius_scaling.ipynb) | 7 | Exaggerates differences quadratically | Scale by area |
| [Bar of means ("dynamite plot")](15_bad_vs_good/dynamite_plot/dynamite_plot.ipynb) | 7 | Hides the distribution and the sample size | Points + confidence interval |
| [Rainbow colour map](15_bad_vs_good/rainbow_colormap/rainbow_colormap.ipynb) | 8 | Creates false bands, not colour-blind safe | One-hue sequential |
| [Unsorted bars](15_bad_vs_good/unsorted_bars/unsorted_bars.ipynb) | 8 | Ranking is hidden | Sort by value |

---

## Pre-publication checklist

The checklist follows the steps. For the full design and storytelling checklist, see
[PRINCIPLES.md](PRINCIPLES.md#checklist).

**A. Message**
- [ ] The audience, the decision and the success metric are known
- [ ] One chart, one message, compared to a target, peer or the past
- [ ] A sentence, number or table wouldn't say it better

**B. Chart choice**
- [ ] The family matches the message (step 4) and the form matches the data (step 5)
- [ ] Denominators, time window and subgroups checked; *n* known
- [ ] Too many series or categories are folded, highlighted or split into small multiples
- [ ] The key comparison uses position or length, not angle, area or colour
- [ ] The chart suits the audience's literacy; unfamiliar charts have a how-to-read note

**C. Drawing**
- [ ] Bars and areas start at zero; any axis break is marked; no dual axes; bubbles scaled by area
- [ ] Log scale used (and labelled) for long-run growth
- [ ] Uncertainty shown for estimates, forecasts and backtests; forecasts dashed; interval type stated
- [ ] The title states the finding; units, period and source are stated
- [ ] Colour has one job, ≤ 6 hues, no rainbow, no red/green-only encoding
- [ ] Series identifiable without colour: direct labels where possible
- [ ] Categories sorted unless they have a natural order
- [ ] Passes the five-second test, at final size and in grayscale
- [ ] Interactive charts still make sense as a static image

---

## Using the library to choose

- **Gallery** (`gallery/index.html`): filter by **Goal** (step 4), **Your data** (step 5) and
  **Level** (step 6), and use **Interactive** / **Animated** for the medium. Each card's
  *Purpose & when to use* lists when **not** to use it.
- **README → Chart chooser:** the data-type mapping as a table.
- **Every notebook:** design purpose, when to use, when to avoid, alternatives, design tips, a worked example and how to read it.
- **README → Methods from the research literature:** peer-reviewed methods, newest first, each with its citation (filter **From research papers** in the gallery).
- **Your own price data:**
  `python -m vizlib.finance prices.csv --price Fund --benchmark Index -o report.png`

### Further reading
- [PRINCIPLES.md](PRINCIPLES.md): perception, design, integrity, statistical traps and storytelling behind every step here
- Financial Times, *Visual Vocabulary*: https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary
- From Data to Viz (decision tree and caveats): https://www.data-to-viz.com
- The Data Visualisation Catalogue: https://datavizcatalogue.com
- data.europa.eu, *Choosing charts: the message*: https://data.europa.eu/apps/data-visualisation-guide/choosing-charts-the-message
- Cole Nussbaumer Knaflic, *Storytelling with Data* (2015)
- Claus O. Wilke, *Fundamentals of Data Visualization* (2019): https://clauswilke.com/dataviz/
- **Research papers behind specific charts:** see [README → Sources → Research papers](README.md#research-papers), generated from each chart's citation
