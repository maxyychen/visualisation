# How to Choose a Chart

A practical guideline for turning data into the right visualization. Every chart named here links
to a worked example in this library: a notebook with its purpose, when to use it, when to avoid it,
and runnable code.

**Short version:** decide what the reader should *notice*, check what your data *supports*, pick the
*simplest* chart that shows it, encode it *honestly*, then *test* it on someone.

---

## Contents

1. [Write the message as one sentence](#step-1-write-the-message-as-one-sentence)
2. [Name the relationship](#step-2-name-the-relationship)
3. [Check what your data supports](#step-3-check-what-your-data-supports)
4. [Match the audience and the medium](#step-4-match-the-audience-and-the-medium)
5. [Encode honestly](#step-5-encode-honestly)
6. [Show uncertainty](#step-6-show-uncertainty)
7. [Test it](#step-7-test-it)
- [Quick decision path](#quick-decision-path)
- [Finance and investment quick reference](#finance-and-investment-quick-reference)
- [Common mistakes and their fixes](#common-mistakes-and-their-fixes)
- [Pre-publication checklist](#pre-publication-checklist)
- [Using the library to choose](#using-the-library-to-choose)

---

## Step 1: Write the message as one sentence

Before you plot anything, finish the sentence **"The reader should see that…"**

| Sentence | What it tells you |
|---|---|
| "…our fund fell less than the index in 2022." | A comparison over time, against a benchmark |
| "…three clients make up 60% of revenue." | Part-to-whole, with the top items emphasised |
| "…daily returns have fatter tails than a normal distribution." | A distribution, compared with a reference |
| "…sales rise with advertising spend." | A relationship between two numbers |

**You can't write the sentence yet?** Then you are **exploring**, not presenting. That is a separate
activity with different charts: make many quick, rough plots (a [histogram](04_distribution/histogram/histogram.ipynb), a
[pair plot](02_correlation/pair_plot/pair_plot.ipynb), a [line chart](05_change_over_time/line_chart/line_chart.ipynb), a [correlation heatmap](02_correlation/correlation_heatmap/correlation_heatmap.ipynb))
and polish nothing until you know what the message is.

> **Rule:** one chart, one message. If you have two messages, make two charts.

---

## Step 2: Name the relationship

The verb in your sentence picks a chart **family**. These nine families follow the Financial Times
*Visual Vocabulary*, plus uncertainty.

| The sentence is about… | Family | Start with | Then consider |
|---|---|---|---|
| A difference from a baseline (target, zero, average) | Deviation | [Diverging bar](01_deviation/diverging_bar/diverging_bar.ipynb) | [Lollipop from mean](01_deviation/deviation_lollipop/deviation_lollipop.ipynb), [surplus/deficit line](01_deviation/surplus_deficit_line/surplus_deficit_line.ipynb) |
| Two or more variables moving together | Correlation | [Scatter](02_correlation/scatter/scatter.ipynb) | [Scatter + regression](02_correlation/scatter_regression/scatter_regression.ipynb), [bubble](02_correlation/bubble/bubble.ipynb), [correlation heatmap](02_correlation/correlation_heatmap/correlation_heatmap.ipynb) |
| Order (who's first, who's last) | Ranking | [Sorted bar](03_ranking/ordered_bar/ordered_bar.ipynb) | [Lollipop](03_ranking/lollipop_ranking/lollipop_ranking.ipynb), [slope chart](03_ranking/slope_chart/slope_chart.ipynb), [bump chart](03_ranking/bump_chart/bump_chart.ipynb) |
| Spread, skew, outliers | Distribution | [Histogram](04_distribution/histogram/histogram.ipynb) | [Box plot](04_distribution/box_plot/box_plot.ipynb), [violin](04_distribution/violin_plot/violin_plot.ipynb), [ECDF](04_distribution/ecdf/ecdf.ipynb) |
| A trend over time | Change over time | [Line chart](05_change_over_time/line_chart/line_chart.ipynb) | [Area](05_change_over_time/area_chart/area_chart.ipynb), [indexed line](05_change_over_time/indexed_line/indexed_line.ipynb), [small multiples](05_change_over_time/small_multiples_line/small_multiples_line.ipynb) |
| A size comparison | Magnitude | [Bar chart](06_magnitude/horizontal_bar/horizontal_bar.ipynb) | [Grouped bar](06_magnitude/grouped_bar/grouped_bar.ipynb), [dumbbell](06_magnitude/dumbbell/dumbbell.ipynb), [bullet chart](06_magnitude/bullet_chart/bullet_chart.ipynb) |
| A share of a total | Part-to-whole | [Stacked bar](07_part_to_whole/stacked_bar/stacked_bar.ipynb) | [100% stacked bar](07_part_to_whole/percent_stacked_bar/percent_stacked_bar.ipynb), [treemap](07_part_to_whole/treemap/treemap.ipynb), [waffle](07_part_to_whole/waffle_chart/waffle_chart.ipynb), [waterfall](07_part_to_whole/waterfall_chart/waterfall_chart.ipynb) |
| A location or geographic pattern | Spatial | [Choropleth](08_spatial/choropleth_world/choropleth_world.ipynb) | [Bubble map](08_spatial/bubble_map/bubble_map.ipynb), [tile grid map](08_spatial/tile_grid_map/tile_grid_map.ipynb), [hex-grid map](08_spatial/hexgrid_map/hexgrid_map.ipynb) |
| Movement between stages or places | Flow | [Sankey](09_flow/sankey/sankey.ipynb) | [Funnel](09_flow/funnel_chart/funnel_chart.ipynb), [chord](09_flow/chord_diagram/chord_diagram.ipynb), [flow map](08_spatial/flow_map/flow_map.ipynb) |
| An estimate, forecast or risk | Uncertainty | [Error bars / CI](11_scientific/error_bar_ci/error_bar_ci.ipynb) | [Fan chart](05_change_over_time/fan_chart/fan_chart.ipynb), [gradient interval](13_uncertainty/gradient_interval/gradient_interval.ipynb), [quantile dot plot](13_uncertainty/quantile_dotplot/quantile_dotplot.ipynb) |

**Is the story a single number?** Then it isn't a chart. Use a [KPI stat tile](06_magnitude/kpi_stat_tile/kpi_stat_tile.ipynb),
optionally with a [sparkline](05_change_over_time/sparklines/sparklines.ipynb) for context. A one-bar chart or a two-slice pie only adds ink.

---

## Step 3: Check what your data supports

### Variable types → chart forms

| You have | Natural forms |
|---|---|
| 1 numeric variable | [Histogram](04_distribution/histogram/histogram.ipynb), [box plot](04_distribution/box_plot/box_plot.ipynb), [ECDF](04_distribution/ecdf/ecdf.ipynb) |
| 1 category + 1 number | [Sorted bar](03_ranking/ordered_bar/ordered_bar.ipynb), [dot plot](03_ranking/cleveland_dot/cleveland_dot.ipynb), [lollipop](03_ranking/lollipop_ranking/lollipop_ranking.ipynb) |
| 1 category + 1 number, by group | [Box plot](04_distribution/box_plot/box_plot.ipynb), [violin](04_distribution/violin_plot/violin_plot.ipynb), [strip/jitter](04_distribution/strip_jitter/strip_jitter.ipynb), [ridgeline](04_distribution/ridgeline/ridgeline.ipynb) |
| 2 numbers | [Scatter](02_correlation/scatter/scatter.ipynb), [hexbin](02_correlation/hexbin/hexbin.ipynb) (many points) |
| 3+ numbers | [Bubble](02_correlation/bubble/bubble.ipynb), [pair plot](02_correlation/pair_plot/pair_plot.ipynb), [parallel coordinates](06_magnitude/parallel_coordinates/parallel_coordinates.ipynb), [PCA biplot](02_correlation/pca_biplot/pca_biplot.ipynb) |
| Time + 1 number | [Line](05_change_over_time/line_chart/line_chart.ipynb), [column](06_magnitude/column_chart/column_chart.ipynb) (discrete periods), [calendar heatmap](05_change_over_time/calendar_heatmap/calendar_heatmap.ipynb) (daily) |
| Time + several numbers | [Line + highlight](05_change_over_time/line_highlight/line_highlight.ipynb), [small multiples](05_change_over_time/small_multiples_line/small_multiples_line.ipynb), [stacked area](05_change_over_time/stacked_area/stacked_area.ipynb) (parts of a total) |
| 2 categories + 1 number | [Grouped bar](06_magnitude/grouped_bar/grouped_bar.ipynb), [highlight table](06_magnitude/highlight_table/highlight_table.ipynb), [heatmap](09_flow/origin_destination_matrix/origin_destination_matrix.ipynb) |
| Parent → child hierarchy | [Treemap](07_part_to_whole/treemap/treemap.ipynb), [sunburst](07_part_to_whole/sunburst/sunburst.ipynb), [icicle](07_part_to_whole/icicle/icicle.ipynb) |
| From → to with amounts | [Sankey](09_flow/sankey/sankey.ipynb), [chord](09_flow/chord_diagram/chord_diagram.ipynb), [origin–destination matrix](09_flow/origin_destination_matrix/origin_destination_matrix.ipynb) |
| Nodes and links | [Network graph](09_flow/network_graph/network_graph.ipynb), [adjacency matrix](09_flow/adjacency_matrix/adjacency_matrix.ipynb) (large networks) |
| Overlapping sets | [Venn](07_part_to_whole/venn_diagram/venn_diagram.ipynb) (≤ 3 sets), [UpSet](11_scientific/upset_plot/upset_plot.ipynb) (more) |
| Locations | [Choropleth](08_spatial/choropleth_world/choropleth_world.ipynb) (regions), [bubble map](08_spatial/bubble_map/bubble_map.ipynb) (points), [hex-grid map](08_spatial/hexgrid_map/hexgrid_map.ipynb) (dense points) |
| Prices or returns | [Cumulative return vs. benchmark](10_finance_investment/cumulative_return_benchmark/cumulative_return_benchmark.ipynb), [drawdown](10_finance_investment/drawdown_underwater/drawdown_underwater.ipynb), [tear sheet](10_finance_investment/performance_tear_sheet/performance_tear_sheet.ipynb) |

### How many things? (the scale check)

Most chart failures are scale failures. Check these before choosing:

| When you have… | The problem | Fix |
|---|---|---|
| More than ~10 categories | Bars and slices become unreadable | Sort, show top-N, fold the rest into "Other", or use a table |
| More than ~4 lines | Spaghetti | [Highlight one, gray the rest](05_change_over_time/line_highlight/line_highlight.ipynb), or [small multiples](05_change_over_time/small_multiples_line/small_multiples_line.ipynb) |
| More than ~5 slices | Pie angles can't be compared | [Sorted bar](03_ranking/ordered_bar/ordered_bar.ipynb) or [stacked bar](07_part_to_whole/stacked_bar/stacked_bar.ipynb) |
| More than ~10,000 points | Overplotting turns into a blob | Transparency → [hexbin](02_correlation/hexbin/hexbin.ipynb) → [datashader](15_interactive_advanced/datashader_scatter/datashader_scatter.ipynb) |
| Measures on different scales | The temptation of a dual axis | [Index to 100](05_change_over_time/indexed_line/indexed_line.ipynb), or stack panels sharing the x-axis ([rolling metrics](10_finance_investment/rolling_metrics/rolling_metrics.ipynb)) |
| More than ~8 colours needed | Hues become indistinguishable | Fold into "Other", facet into small multiples, or label directly |

---

## Step 4: Match the audience and the medium

### Audience

| Audience | Prefer | Avoid |
|---|---|---|
| Executives, clients, board | **Basic** charts (bar, line, stat tile); one message each; the conclusion as the title; the key number labelled | Dense multi-panel charts, unexplained jargon |
| Analysts, investment committee | **Intermediate** charts (small multiples, heatmaps, distributions, intervals) | Oversimplification that hides risk |
| Specialists, research | **Advanced** charts ([HRP dendrogram](10_finance_investment/hrp_dendrogram/hrp_dendrogram.ipynb), [regime shading](10_finance_investment/regime_shading/regime_shading.ipynb), [event study](10_finance_investment/event_study/event_study.ipynb)) | Using them on a general audience without explanation |

**Titles state the finding.** "Fund beat the index in 4 of 5 down years" helps the reader more than
"Annual returns 2019–2024".

### Medium: static, interactive or animated?

| Choose | When | Library examples |
|---|---|---|
| **Static** (the default) | Reports, slides, print, decisions: anything that must say one thing reliably | Almost everything |
| **Interactive** | Readers need *their own* what-if, or their own slice of a large dataset | [Option payoff explorer](15_interactive_advanced/option_payoff_explorer/option_payoff_explorer.ipynb), [linked price & returns](15_interactive_advanced/linked_price_returns/linked_price_returns.ipynb), [crossfilter dashboard](15_interactive_advanced/crossfilter_dashboard/crossfilter_dashboard.ipynb) |
| **Animated** | The motion itself is the story (a curve inverting, a ranking reshuffling), usually in a presentation | [Animated yield curve](15_interactive_advanced/animated_yield_curve/animated_yield_curve.ipynb), [bar-chart race](15_interactive_advanced/bar_chart_race/bar_chart_race.ipynb) |

To **compare** across time, [small multiples beat animation](14_bad_vs_good/animation_vs_small_multiples/animation_vs_small_multiples.ipynb): with
animation, readers must remember earlier frames. Every interactive chart should also work as a
static image of its default state.

---

## Step 5: Encode honestly

### Position, length and scale
- **Bars start at zero.** Bar length is the value, so a cut axis exaggerates differences ([see why](14_bad_vs_good/truncated_bar_axis/truncated_bar_axis.ipynb)).
  Lines and dots can zoom in, because position carries the value.
- **Use a log scale for long-run growth** (prices, wealth, GDP) so that equal percentage moves look equal.
- **Sort categories** by value unless they have a natural order such as time, age bands or ratings ([see why](14_bad_vs_good/unsorted_bars/unsorted_bars.ipynb)).
- **Size encodes area, not radius.** A bubble twice the value should have twice the area ([see why](14_bad_vs_good/bubble_radius_scaling/bubble_radius_scaling.ipynb)).
- **One y-axis per panel.** Never a dual axis ([see why](14_bad_vs_good/dual_axis_vs_indexed/dual_axis_vs_indexed.ipynb)).

### Colour: assign it by the job it does

| Job | Rule | Example |
|---|---|---|
| **Identity** (which series) | Distinct hues in a fixed order, ≤ 8; colour follows the entity, never its rank | [Line chart](05_change_over_time/line_chart/line_chart.ipynb) |
| **Magnitude** (how much) | One hue, light → dark | [Highlight table](06_magnitude/highlight_table/highlight_table.ipynb), [choropleth](08_spatial/choropleth_world/choropleth_world.ipynb) |
| **Polarity** (above/below, gain/loss) | Two opposite hues around a neutral gray midpoint | [Monthly returns heatmap](10_finance_investment/monthly_returns_heatmap/monthly_returns_heatmap.ipynb) |
| **Emphasis** (this one matters) | One accent colour, everything else gray | [Line highlight](05_change_over_time/line_highlight/line_highlight.ipynb), [sorted bar](03_ranking/ordered_bar/ordered_bar.ipynb) |

- Never use a rainbow colour map ([see why](14_bad_vs_good/rainbow_colormap/rainbow_colormap.ipynb)). It invents boundaries and fails for colour-blind readers.
- Don't rely on red/green alone for gains and losses. Blue/orange is colour-blind-safe; add signs (+/−) or labels too.
- Text stays in neutral ink. Colour the mark, not the label.

### Labels and clutter
- Label directly (at line ends, beside bars) instead of making readers decode a legend.
- Label **selectively**: the endpoint, the maximum, the one that matters. Never a number on every point.
- Use hairline, recessive gridlines; no 3-D effects, shadows or heavy borders.

---

## Step 6: Show uncertainty

If a number is an **estimate, forecast, backtest or sample**, show its range. A single line claims
more certainty than you have.

| Situation | Chart |
|---|---|
| Group means or effects | [Points + 95% CI](11_scientific/error_bar_ci/error_bar_ci.ipynb), not a bar of means ([see why](14_bad_vs_good/dynamite_plot/dynamite_plot.ipynb)) |
| A forecast | [Fan chart](05_change_over_time/fan_chart/fan_chart.ipynb), [Monte Carlo wealth paths](10_finance_investment/monte_carlo_wealth/monte_carlo_wealth.ipynb) |
| Several estimates, compared | [Gradient interval](13_uncertainty/gradient_interval/gradient_interval.ipynb), [half-eye plot](13_uncertainty/half_eye/half_eye.ipynb), [forest plot](11_scientific/forest_plot/forest_plot.ipynb) |
| Risk for a non-technical audience | [Icon array](13_uncertainty/icon_array/icon_array.ipynb) ("7 in 100"), [quantile dot plot](13_uncertainty/quantile_dotplot/quantile_dotplot.ipynb) |
| Tail risk | [Return distribution with VaR/CVaR](10_finance_investment/return_distribution_var/return_distribution_var.ipynb) |

---

## Step 7: Test it

**The five-second test:** show the chart to someone for five seconds, then ask "what did you see?"
If the answer isn't your sentence from step 1, simplify, in this order:

1. Remove series or categories that don't serve the message.
2. Sort the bars.
3. Replace the legend with direct labels.
4. Gray everything except what matters.
5. Move the message into the title.
6. Still not working? Pick a different chart from the same family.

---

## Quick decision path

```
Is the story a single number?          → KPI stat tile (+ sparkline)
Is it about change over time?
    ≤ 4 series                         → line chart
    one series matters                 → line + highlight (others gray)
    many series                        → small multiples
    different units/scales             → indexed line (= 100 at start)
    parts of a total over time         → stacked area
Comparing categories?
    one measure                        → sorted bar / dot plot
    two time points                    → dumbbell or slope chart
    two measures per category          → grouped bar
    against a target                   → bullet chart / diverging bar
Shares of a total?
    ≤ 5 parts                          → stacked bar (pie/donut acceptable)
    hierarchy                          → treemap / sunburst
    how a total got from A to B        → waterfall
Relationship between numbers?
    two numbers                        → scatter (+ trend line)
    > 10k points                       → hexbin → datashader
    many variables                     → correlation heatmap / pair plot
Shape of values?
    one group                          → histogram
    several groups                     → box / violin / ridgeline
    comparing percentiles              → ECDF
Risk, estimates or forecasts?          → CI dots / fan chart / VaR distribution
Movement between stages or places?     → funnel (one path) / sankey (branches) / flow map
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
| How do assets cluster? | [Correlation heatmap](02_correlation/correlation_heatmap/correlation_heatmap.ipynb), [correlation network](10_finance_investment/correlation_network_mst/correlation_network_mst.ipynb), [HRP dendrogram](10_finance_investment/hrp_dendrogram/hrp_dendrogram.ipynb) |
| What is the market doing? | [Candlestick + moving averages](10_finance_investment/candlestick_ma_volume/candlestick_ma_volume.ipynb), [sector heatmap](10_finance_investment/sector_heatmap/sector_heatmap.ipynb), [market breadth](10_finance_investment/market_breadth/market_breadth.ipynb) |
| What are rates telling us? | [Yield curve](10_finance_investment/yield_curve/yield_curve.ipynb), [yield curve history](10_finance_investment/yield_curve_history/yield_curve_history.ipynb), [animated yield curve](15_interactive_advanced/animated_yield_curve/animated_yield_curve.ipynb) |
| What does this option position do? | [Option payoff](10_finance_investment/option_payoff/option_payoff.ipynb), [option payoff explorer](15_interactive_advanced/option_payoff_explorer/option_payoff_explorer.ipynb) (interactive) |
| What is the company worth? | [Football field](10_finance_investment/football_field_valuation/football_field_valuation.ipynb), [DCF sensitivity table](10_finance_investment/dcf_sensitivity_table/dcf_sensitivity_table.ipynb), [DCF explorer](15_interactive_advanced/dcf_explorer/dcf_explorer.ipynb) |
| Where does the revenue go, and why did it change? | [Income statement sankey](10_finance_investment/income_statement_sankey/income_statement_sankey.ipynb), [revenue bridge](10_finance_investment/revenue_bridge/revenue_bridge.ipynb), [waterfall](07_part_to_whole/waterfall_chart/waterfall_chart.ipynb) |
| Will the money last? | [Monte Carlo wealth](10_finance_investment/monte_carlo_wealth/monte_carlo_wealth.ipynb), [retirement planner](15_interactive_advanced/retirement_planner/retirement_planner.ipynb) (interactive) |
| Lump sum or dollar-cost averaging? | [Compounding & DCA](10_finance_investment/compounding_dca/compounding_dca.ipynb) |

Finance-specific rules:
- Compare performance against a benchmark, net of fees, over the **same** period.
- Show **risk next to return**, never return alone.
- Use log scales for long histories and **index** series to a common start (= 100) when comparing.
- Pick the start date honestly; a cherry-picked start date is the most common way performance charts mislead.
- Mark simulated or backtested results as such.

---

## Common mistakes and their fixes

Each links to a side-by-side example in the **Bad vs. good** family.

| Mistake | Why it misleads | Fix |
|---|---|---|
| [Dual y-axis](14_bad_vs_good/dual_axis_vs_indexed/dual_axis_vs_indexed.ipynb) | Axis ranges are arbitrary, so crossings and slopes are invented | Index to 100, or two panels |
| [Truncated bar axis](14_bad_vs_good/truncated_bar_axis/truncated_bar_axis.ipynb) | Small differences look huge | Start bars at zero, or use dots |
| [Pie with close values](14_bad_vs_good/pie_close_values/pie_close_values.ipynb) | Angles can't be compared | Sorted bar |
| [Rainbow colour map](14_bad_vs_good/rainbow_colormap/rainbow_colormap.ipynb) | Creates false bands, not colour-blind safe | One-hue sequential |
| [Spaghetti lines](14_bad_vs_good/spaghetti_vs_highlight/spaghetti_vs_highlight.ipynb) | Nothing stands out | Highlight one, gray the rest |
| [Unsorted bars](14_bad_vs_good/unsorted_bars/unsorted_bars.ipynb) | Ranking is hidden | Sort by value |
| [Overplotting](14_bad_vs_good/overplotting/overplotting.ipynb) | Density is invisible | Transparency, hexbin, datashader |
| [Bar of means ("dynamite plot")](14_bad_vs_good/dynamite_plot/dynamite_plot.ipynb) | Hides the distribution and the sample size | Points + confidence interval |
| [Bubbles scaled by radius](14_bad_vs_good/bubble_radius_scaling/bubble_radius_scaling.ipynb) | Exaggerates differences quadratically | Scale by area |
| [Animation for comparison](14_bad_vs_good/animation_vs_small_multiples/animation_vs_small_multiples.ipynb) | Relies on memory | Small multiples |

---

## Pre-publication checklist

**Message**
- [ ] The title states the finding, not just the topic
- [ ] One chart, one message
- [ ] The chart passes the five-second test

**Form**
- [ ] The chart type matches the relationship (step 2) and the data (step 3)
- [ ] Categories are sorted unless they have a natural order
- [ ] Too many series or categories are folded, highlighted or split into small multiples

**Honesty**
- [ ] Bars start at zero; no dual axes; area-scaled bubbles
- [ ] Log scale used (and labelled) for long-run growth
- [ ] Uncertainty is shown for estimates, forecasts and backtests
- [ ] The time window is not cherry-picked; benchmark and period are stated

**Colour and labels**
- [ ] Colour has a job (identity, magnitude, polarity or emphasis), with ≤ 8 hues
- [ ] No rainbow; no red/green-only encoding
- [ ] Direct labels where possible; a legend whenever there are ≥ 2 series
- [ ] Units, currency and data source are stated

**Delivery**
- [ ] Readable at its final size (slide, page, phone)
- [ ] Works in grayscale or for colour-blind readers (add labels or patterns if not)
- [ ] Interactive charts still make sense as a static image

---

## Using the library to choose

- **Gallery** (`gallery/index.html`): filter by **Goal** (step 2), **Your data** (step 3) and
  **Level** (step 4), and use **Interactive** / **Animated** for the medium. Each card's
  *Purpose & when to use* lists when **not** to use it.
- **README → Chart chooser:** the data-type mapping as a table.
- **Every notebook:** design purpose, when to use, when to avoid, alternatives, design tips, a worked example and how to read it.
- **Your own price data:**
  `python -m vizlib.finance prices.csv --price Fund --benchmark Index -o report.png`

### Further reading
- Financial Times, *Visual Vocabulary*: https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary
- From Data to Viz (decision tree and caveats): https://www.data-to-viz.com
- The Data Visualisation Catalogue: https://datavizcatalogue.com
- data.europa.eu, *Choosing charts: the message*: https://data.europa.eu/apps/data-visualisation-guide/choosing-charts-the-message
- Cole Nussbaumer Knaflic, *Storytelling with Data* (2015)
- Claus O. Wilke, *Fundamentals of Data Visualization* (2019): https://clauswilke.com/dataviz/
