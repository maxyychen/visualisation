# Data Visualization and Storytelling: Core Concepts

---

## 1. What visualization is for

### Three ways to deliver a message

| Format | What you get | Problem |
|---|---|---|
| Raw table | Every number | No message |
| Words only | A clear claim | No evidence |
| Chart + insight title + annotation | Claim and evidence together | None, if done well |

**The data proves the claim; the visual makes it understandable.** Visualization turns data into meaning and cuts the time it takes to understand information. The chart is only the vehicle. What matters is the communication.

### Three related ideas

- **Data visualization**: any visual display of data (points, lines, bars, a single number).
- **Data communication**: one or more visualizations combined with design elements to deliver a message (reports, dashboards, presentations).
- **Data storytelling**: turning data into a narrative that leads an audience to a specific conclusion or action.

Storytelling has less to do with statistics than with visual thinking and narrative.

### Why many charts fail

- **Weak quantitative skill**: making data look nice at the cost of accuracy.
- **Believing data is boring**: adding decoration that distracts or distorts. If the data is boring, you have the wrong data.
- **Underestimating the audience**: simplifying until nothing is left.
- **Plotting on autopilot**: accepting software defaults without thinking.

These lead to **chartjunk**: decoration that makes up for a lack of meaning.

### Form and function

A functional chart doesn't have to be boring, and a beautiful chart doesn't have to be complicated. A chart can fail by looking striking and saying nothing, or by being accurate and impossible to read.

### The recipe

1. Start with good data.
2. Know **why** you're presenting it and **who** it's for.
3. Respect the data: no distortion, no statistical traps.
4. Choose the right format (sentence, number, table or chart).
5. Design on purpose: declutter, use color with intent, title the insight, annotate.
6. End with what to do next.

---

## 2. How people perceive charts

### Encoding and decoding

- **Encoding** (creator): mapping a number to a visual property such as position, length, angle, area or color.
- **Decoding** (viewer): turning the shape back into a number or conclusion.

**A visualization fails if decoding fails**, however clever the encoding. The eye is an imperfect sensor. A bar 30% shorter than its neighbor on a shared baseline is easy to see. A circle 30% smaller is hard to judge.

### Perceptual accuracy ranking

From most to least accurate:

1. **Position on a common scale** (dot plots, scatter plots, bar ends)
2. **Position on non-aligned scales** (upper segments of stacked bars, panels with different axes)
3. **Length, direction, angle**
4. **Area**
5. **Volume, curvature**
6. **Shading, color saturation and hue**

**Rule:** encode with tasks as high on the list as you can, and use as few tasks as you can. Treat this as a guide, not dogma. Use a map when geography is the point.

What follows from the ranking:

- **Stacked bars**: only the bottom segment sits on a shared baseline. The segments above it are hard to compare.
- **Pie charts** rely on angle and area. Values of 41%, 39% and 20% look almost the same as slices but clearly different as bars.
- **Area** differences of 5% are invisible, and even 50% is hard to estimate. Area grows with the square of the radius: 2.5× the radius is 6.25× the area.
- **3D** makes the brain compute depth, and nearer objects look bigger.
- **Gauges and donuts** bend the scale into an arc, which makes precise reading hard.
- **Color** is the least reliable. The same grey looks different on different backgrounds, and color-vision deficiencies change what people see.
- **Combined tasks** add difficulty. A radial bar is length plus curvature. A rotated bar adds a meaningless direction.
- **The curvature trap**: to judge the gap between two lines, people measure the shortest distance between the curves instead of the vertical gap. **If the difference matters, plot the difference.**

### Redesigning up the ranking

- Pie → bar → lollipop/dot (angle and area → length → position)
- Stacked bar → grouped bar → grouped dots (every value on a shared baseline)
- Shaded map → bars or spikes per region (shading → position)

### Built-in perceptual bias

Perceived size ≈ actual size raised to a power below 1 for areas, so people **consistently underestimate areas**. Decoration and 3D make this worse.

### Five perception concepts

1. **Order**: text has a reading order and images don't. Each viewer's eye wanders differently, and many skip the title. Design the chart to guide the eye.
2. **Hierarchy**: the eye goes first to what stands out (bright colors, outliers, big differences). Mute the frame and emphasize the message. Common mistakes are emphasizing axes over data, making everything compete, and highlighting the wrong story (a one-month dip instead of a year of growth).
3. **Clarity**: working memory is small. Viewers turn many points into one trend and remember only the **first two or three things they notice**. Put the story in front.
4. **Relationships**: viewers invent causal stories from whatever sits side by side, and warnings don't stop them. **Show only elements that are actually related.**
5. **Convention**: north is up, red is bad or stop, green is good or go, titles sit at the top. Break a convention and viewers stop trusting the information, not just the layout.

### Gestalt principles in charts

| Principle | Meaning | Chart implication |
|---|---|---|
| **Similarity** | Same color, shape or size reads as a group | The coloring decides which comparisons people make. An odd color marks an exception. |
| **Continuation** | The eye follows smooth paths | Viewers extrapolate lines, and empty future axis space invites a forecast. |
| **Closure** | The brain fills gaps | Viewers imagine points that are missing. |
| **Proximity** | Things close together seem related | Put bars that should be compared next to each other. |
| **Figure/ground** | The foreground gets attention | Bring key data forward with color and push the rest back. |
| **Simplicity** | The brain picks the simplest interpretation | Dense points read as one trend. Use similarity or figure/ground to make points stand out. |

These principles act on every chart, whether you plan for them or not.

---

## 3. Core design principles

### Graphical excellence

Communicate complex ideas with **clarity, precision and efficiency**. A good graphic:

- shows the data;
- keeps attention on the substance, not the design;
- doesn't distort;
- packs many numbers into a small space and makes large datasets coherent;
- invites comparison;
- reveals the data at several levels, from overview to detail;
- has a clear purpose;
- fits with the surrounding text and statistics.

> **Maximize ideas while minimizing the reader's time, the ink and the space.**

### Data-ink ratio

```
Data-ink ratio = ink that encodes data / total ink
```

Data-ink is ink you can't erase without losing information. Readers assume every mark means something.

1. Above all, show the data.
2. Maximize the data-ink ratio.
3. Erase non-data ink (heavy grids, boxes, backgrounds, shadows), within reason.
4. Erase redundant data-ink (axis *or* value labels, not both).
5. Revise and edit.

The "within reason" matters: **a minimal chart nobody understands has failed.** Sometimes ink has to go back in to make the chart readable.

Ink-saving techniques: lollipops instead of bars, range frames (axes that span only the data), lightened grids, thin white borders on maps.

**Typical cleanup sequence:** remove 3D → lighten or remove gridlines → remove shadows → plain background → fit the axis to the data (bars still start at 0) → label values directly → drop a redundant legend → one neutral color plus a highlight → sort → consider a lollipop.

### Data density

```
Data density = number of data entries / area of graphic
```

Maximize density within reason, since most charts can shrink without losing anything. **Very low density means a sentence or a table would do better.**

### Aspect ratio and orientation

- **Wide** charts read left to right, which suits time. **Tall** charts read top to bottom. **Square** charts have no preferred direction.
- A good default is about **1:1.6** (the golden ratio).
- **Banking to 45°**: for line charts, pick the aspect ratio that brings average slopes near 45°, where changes in slope are easiest to see. Different ratios reveal different patterns, such as cycles that rise faster than they fall. The same line looks calm when wide and dramatic when tall, so the ratio is an editorial choice.

---

## 4. Choosing the format

### Do you need a chart?

| Situation | Best format |
|---|---|
| One or two values | A sentence or **one big number** |
| Exact values matter | A table |
| Trends, patterns, comparisons | A chart |

When the audience already has context, one number can be the strongest visualization. **The number does the speaking; the chart is only its container.**

### Chart anatomy

Title, subtitle, source, data marks, series, data labels, axes and legend. Each one can be edited to support the story.

### Chart families by purpose

| Purpose | Question | Good choices | Use carefully or avoid |
|---|---|---|---|
| Change over time | Up, down, flat? | Line, connected scatter, column, slope graph | Area, stacked area, spaghetti |
| Comparison / ranking | Who leads, by how much? | Sorted bar, lollipop, dumbbell, grouped bar, slope graph | Stacked bar, circular bar, radar, word cloud, pictograms |
| Relationship | How does X relate to Y? | Scatter, bubble, heatmap, combo | Lines across categories, 3D |
| Distribution | Spread, shape, outliers? | Histogram, density, boxplot, violin, ridgeline | Bar + error bar ("dynamite") |
| Part-to-whole | How is the total split? | Stacked bar (few parts), waffle, treemap, waterfall | Pie, 3D or exploded pie, donut |
| Spatial | Where? | Bubble, spike, hexbin, cartogram, per-region indicators | Unnormalized shaded maps |
| Status | How close to target? | Gauge, formatted table, big number | |

### Time series

- **Line chart**: the slope is the message. About four lines is the practical maximum.
- **Spaghetti fix**: highlight one or a few lines and grey the rest, or use **small multiples** where each panel highlights its own series against the others in grey.
- **Sparse data**: use a connected scatter so readers can see where the observations are.
- **Never join categories with a line.** A line implies continuity.
- **Area fill** under a line usually adds meaningless ink. **Stacked areas** lose the shared baseline, so they work only when the total is what matters. **Overlapping areas** hide each other. Always say whether a chart is stacked or overlapping.
- **Slope graph**: before/after for many items, and good for showing changes in rank.

### Comparison

- **Bar chart**: the workhorse, because aligned length is judged accurately. Start at zero, sort, use thin bars, prefer grouped to stacked, go horizontal for long labels.
- **Lollipop**: less ink and no area cue.
- **Dumbbell / dot plot**: two values per item, or a min–max range.
- **Parallel coordinates**: many variables. Worth it only when there's a pattern. Use thin lines and order the axes so fewer lines cross.
- **Avoid**: circular bars (several hard tasks at once), radar charts (the shape depends on axis order and draws attention to area), word clouds (long words look important).

### Relationships

- **Scatter**: correlation can be positive, negative or absent; linear or curved; strong or weak. Watch for spurious correlation and overplotting (use transparency or jitter).
- **Bubble**: the third variable goes on **area, not radius**. Size is the least accurate channel, so give it the least important variable. Use transparency so big bubbles don't hide small ones.
- **Heatmap**: a matrix shown as color. Good for patterns, poor for exact values.
- **Combo / dual axis**: color-match each series to its axis. The two axes are independent, so stretching one can make any change look trivial or alarming. Use a single shared axis whenever the metrics allow it.

### Distributions

- **Histogram**: counts per bin, with touching bars. **It is not a bar chart.** Try several bin widths, because the conclusion can change.
- **Density plot**: a smoothed histogram where y means likelihood, not volume. A falling tail means fewer cases at that value, not a decline over time.
- **Boxplot**: median, IQR, whiskers and outliers, but it **hides sample size**. Overlay the raw points when you can.
- **Violin**: a mirrored density. Show *n*, and order by median unless the groups have a natural order.
- **Ridgeline**: works only for a few groups with a clear pattern.

### Part-to-whole

- **Pie charts** are a poor choice in almost every case, and a bar chart is nearly always clearer. Angles and areas are hard to compare, every slice needs a label, there's no white space for highlights or annotations, and the circle is always the same size, so totals can't be compared across pies. 3D, tilted and exploded versions are worse. Donuts have the same problems. At most, use a pie for two or three simple shares.
- **Stacked bar**: fine with a few parts and no tiny segments.
- **Treemap**: many segments and sub-groups, for approximate proportions.
- **Waterfall**: the **journey from one total to another** (start → increases → decreases → end), for profit bridges, inventory, membership counts and similar.
- **Dendrogram**: hierarchy.

### Maps

- Start from an accurate base map. Wrong borders damage credibility.
- **Shaded (choropleth) maps** let big regions dominate and small important ones vanish. Normalize by population or area, and remember maps show broad patterns, not small differences.
- Alternatives: hexbin or tile maps, cartograms, bubble or spike maps, indicators per region.
- Match the map to the question. "Who won?" calls for winner colors. "How did people vote?" calls for a gradient or population-sized marks.

### Underrated options

- **Gauge**: current value against a target in a small space. It can't show trends, and the arc is hard to read precisely.
- **Formatted table** with a color scale: good for many data points where outliers matter, or many metrics for one series.
- **One big number.**

### Dashboard vs. single chart

- **One focused chart** is the way to prove one point.
- **Dashboards** give an overview, but they dilute focus, can let a good metric hide a bad one, and add cognitive load. Use them for awareness, and single charts for decisions.

---

## 5. Designing the chart

### Declutter

Clutter is anything that doesn't support the message. **Delete everything, then add back only what is needed to understand the chart.**

- Keep the category labels. Replace the value axis with data labels where you can.
- Remove redundant legends, or label lines and bars directly.
- Remove or soften gridlines, backgrounds, borders, shadows and 3D.
- Grey out everything except the data you're discussing.
- Simplify crowded time axes (Q1–Q4 with one year label per group).
- Shorten category names.
- Choosing a chart and decluttering it are iterative. Changing type can mean adding elements back.

### Labels and axes

- Label directly. You don't need to label every point; for a trend, the start and end are often enough.
- State units once ("Users (thousands)"). Always say what's measured.
- Abbreviate large numbers ($18M), keep text horizontal, use sparse tick intervals.
- Use a **detail view**: a zoomed inset of the critical segment next to the main chart.

### Color with purpose

"It looks nice" is not a reason. Color has five legitimate jobs:

1. **Hierarchy**: grey the background and brighten the story.
2. **Encoding an extra variable**, for example coloring bars by *met vs. missed target*.
3. **Reinforcing** a variable already shown, like a temperature line running from blue to red.
4. **Convention**: red is bad, green is good, water is blue, dark means more.
5. **Relationships**: similar colors invite comparison, so color by whatever you want compared.

**Palette types.** Start by asking how the values relate to each other.

| Palette | When | Notes |
|---|---|---|
| **Categorical** | Unordered groups | About 6 colors maximum |
| **Sequential** | Low → high | Light = low, dark = high |
| **Diverging** | Meaningful midpoint (zero, average, target) | Light center, two hues out |

Common mistakes:

- **Rainbow bars**: readers look for a meaning that isn't there, and every bar competes.
- **The most important variable on color**: color is the least accurate channel, so put the key variable on position or length.
- **Inconsistency**: one entity should get one color across every chart, and that color shouldn't mean anything else.
- **Ignoring color blindness** (about 5% of people): use colorblind-safe palettes and test in grayscale.
- **Brand palettes** that contain red/green or clashing hues.

**Safe default:** grey for context, one data color, one neutral accent (orange or yellow) for the highlight, and red/green only when good/bad is the message.

### Annotations

> The chart shows *what* happened. The annotation explains *why*.

Annotations speak for you when you aren't in the room. Use them to:

- mark events (launches, policy changes);
- shade periods;
- explain how to read an unfamiliar chart;
- show changes so readers don't have to calculate them ("+2.1% YoY");
- point to the key takeaway at the final data point.

Annotate only what matters. A dense cluster of labels makes an area *look* important.

Callouts come in two forms: a **short, muted written summary** beside the chart, and **direct annotations** on the data.

### Uncertainty

- **Forecasts are never solid lines.** Use dashed lines, lighter tones or hatched fills, an "estimate" marker and a note. Dashes survive print and grayscale. Scenarios can fan out from the last actual value.
- Distinguish "no data" from "forecast."
- **Error bars**: always state what they show (standard deviation, standard error, confidence interval or min–max), because they look identical and mean different things.
- **Avoid dynamite plots** (bar plus error bar): the bar hides half the error bar and fills space where there is no data. Show raw points, dot plus interval, a boxplot or a violin instead.

---

## 6. Graphical integrity

A **misleading chart** shows accurate data in a way that leads to a false conclusion, whether on purpose or by accident (software auto-truncates axes).

### Proportionality and the Lie Factor

Visual size should be directly proportional to the numbers it represents.

```
Lie Factor = effect size shown in graphic / effect size in data
effect = (larger − smaller) / smaller
```

- **≈ 1**: honest
- **> 1**: exaggerates
- **< 1**: understates

Measure what the reader actually decodes: length for bars, area for bubbles, volume for 3D shapes.

**The classic trap is scaling icons in two dimensions for one-dimensional data.** If a value doubles and the icon doubles in both width and height, its area grows 4×, a Lie Factor of 3.

### Integrity principles

1. **Proportional representation** (above).
2. **Clear, thorough labeling** removes distortion and ambiguity.
3. **Show data variation, not design variation.** Don't mix interval lengths (a partial year beside full years, a shorter final bin), don't change scales partway, and adjust money for inflation. Compare like with like.
4. **Don't show more dimensions than the data has.** Area, color, perspective and 3D can all add dimensions the data doesn't have.

### 3D

Decorative 3D adds clutter, encodes nothing, has no standard way to be read (front face, back face or gridline?) and distorts through perspective. Use 3D only if every answer below favors it:

1. Is it needed, or does it just look nice?
2. Does the data really have three dimensions, or is it 2D with several instances (use several 2D plots)?
3. Does the relationship among all three variables matter?
4. Could the third variable go on color, shape or size instead?
5. Is the 3D version actually easy to read?
6. Does the data naturally live in 3D, like a surface?

### When can the y-axis skip zero?

| Chart | Reader decodes | Zero baseline |
|---|---|---|
| Bar, lollipop | Length | **Required** |
| Shaded area, density | Area | **Required** |
| Line, dot, scatter | Position | **Optional**: choose a sensible range |

- A truncated bar axis is the most common distortion, and viewers overestimate the difference even when the break is marked.
- For lines: **if zero is nearby, include it.**
- Axis range works in both directions. A huge range flattens a real trend, and a tight one exaggerates noise. Be suspicious of any chart whose point is how flat or how volatile a line looks.
- Shade under a line only when the area *is* the data.
- Don't move the baseline to an arbitrary reference value.
- **If you must break a bar axis, make the break obvious** with a labeled zero and break marks on the axis and on every broken bar.

### Other distortions

- Stretched or squashed plot dimensions change how steep slopes look.
- Bars with no scale can be drawn any size.
- **Inverted axes** (zero at the top) make a rise look like a fall.
- **Cherry-picked time windows** hide the longer pattern.
- **Averages** hide extremes.
- **Hand-drawn infographics** are only as honest as their author.

### Defending yourself as a reader

Check axes and scales, ask what lies outside the time window and what else could explain the change, be skeptical of charts with an agenda, go to the source data, and build your own chart when you can.

---

## 7. Statistical traps

Sometimes the chart is fine and the **data** is the problem.

### Correlation vs. causation

Correlation is necessary for causation but not sufficient. A correlation between A and B can come from:

- **A → B**
- **B → A** (reverse causation)
- **A ↔ B** (a feedback loop)
- **A hidden third variable C** driving both
- **Coincidence** (spurious correlation)

Rescaling one axis can make unrelated series appear to match. Viewers also infer causation from whatever you put side by side.

### Sampling biases

- **Selection bias**: the sample differs systematically from the population. A sample doesn't need to be perfectly random, but it must be random *with respect to the question*.
- **Attrition bias**: dropouts aren't random, so results describe only the survivors. A study that excludes people who haven't reached the outcome yet produces false trends, such as newer groups appearing to have shorter lifespans because their long-lived members are still alive.

### "Compared to what?"

- Two data points can tell any story. A longer series may show the "before" value was an outlier, or that the same change happened everywhere.
- **Include the zero-event cases.** Looking only at failures can hide the pattern that separates failures from successes.
- **Never show a number alone.** Compare it to a goal, a peer or the past.

### Normalization

Using the wrong denominator is nearly invisible and very common.

- Use per-capita rates across regions, not totals.
- Adjust money over time for inflation.
- Make sure both sides use the same denominator (per store vs. per employee).
- Raw counts can reflect how hard you looked (testing volume, for example).

Always check *n* and always label the unit.

### Simpson's paradox

A trend that holds within every subgroup can **disappear or reverse** when the groups are combined, usually because the groups differ in size or mix. **Plot subgroups separately before drawing conclusions from the total.**

---

## 8. Data storytelling

### A chart is not a story

A clean chart can still leave the audience asking whether this is good, why something happened and what to do. A story adds design elements (color, emphasis, text) that build a narrative and that the numbers support. **Every element should support the same message.**

### The analytics value chain

**Data → (analysis) → Information → (+ context) → Insight → Decision → Result**

- *Information*: a fact with no judgment ("this store charges $28").
- *Insight*: a fact plus context that implies an action ("lowest price, lowest earnings, and customers will pay more, so raise the price").

Presenting information without insight is handing the audience an unassembled jigsaw puzzle. Assembling it is the analyst's job.

### Context: who and what

- **Who**: group the audience by their **perspective on the data** (finance vs. operations, for example). Different perspectives may need different versions of the story.
- **What**: what should they know or do? Frame the analysis around the **levers** they can actually pull.
- "We need more analysis" is a valid outcome if you say what data would help.

### Consult for context, every time

Requesters assume you share their context. Ask them:

- What questions do you want answered?
- What do you expect to find, or what should I look out for?
- What's the background, and why is this needed now?

**Find the real success metric.** A report can be entirely correct and still recommend the wrong option because it measured the wrong thing, for example clicks when the goal was quality applicants.

### Framing

The same data can be framed as reassurance ("average delivery is 3 days") or as a problem to fix ("1 in 10 orders takes twice as long as promised"). Leaving out the uncomfortable part is lying with data.

- **The "so what?" test**: the point should be clear within about five seconds.
- **Context**: compare to a target, a peer or the past.
- **Hero or villain**: every chart has a main character, so highlight it.
- **Time window**: choose it deliberately and don't cherry-pick.

### Titles that state the insight

Many readers see only the title, so it should carry the conclusion.

- Weak: "Operating cost per unit by location"
- Better: "City A costs $82 per unit while City B costs $38"
- Strong: "13 hubs exceed the $50 cost target" (with the target line drawn on the chart)

**Question titles** ("Did X change Y?") also work: they draw people in and promise an answer. Add a subtitle for context when needed.

### Strengthening the narrative

- Lead with the takeaway.
- Draw a **target or benchmark line** (dashed).
- Split colors into "needs attention" and "fine."
- Add **two or three indicators**, contextual numbers that translate data into impact ("+45% growth → ~$1.2M potential").
- Add a short written summary and direct annotations.
- Add a zoomed **detail chart** of the critical segment.
- Use bolder annotations for live presentations and lighter ones for print.

### Story arcs

Match the message to an arc. The arc tells you where to put the focus.

| Arc | Message | Design |
|---|---|---|
| **Underdog** | Something overcame a challenge | Highlight the hero, add a "+X%" indicator, mute the rest |
| **Redemption** | One factor offers hope | Highlight that opportunity and its potential impact |
| **Betrayal** | An external threat or underperformance | Red for the threat and its impact, nothing extra |
| **Victory** | Success | Big, bold green numbers, often with no chart |
| **Tragedy** | A plainly negative result | Big, bold red numbers |
| **Comparison** | Choosing among options | Equal treatment except for the winner |
| **Influence** | Before / during / after an event | Shade the event period |

Arcs shape the structure, not the specific chart type.

### Six steps to a data story

1. **What's the point?** Consult the audience, learn their perspective, pick an arc.
2. **Pick the format**: chart, number, sentence or table.
3. **Edit for clarity**: start from nothing and add only what helps.
4. **Format for impact**: bright vs. muted, a clear foreground, meaningful color.
5. **Format for narrative**: insight title, indicators, direct labels, a short summary.
6. **What's next?** End with actions. Analysis exists to drive decisions.

---

## 9. Lessons from worked examples

- **Don't replace a dense report that works; pair it with a short story.** A reference report serves people who have context. A focused story carries this period's one or two messages.
- **Build a chart in layers**: default → remove axis and legend → color the focus → add a target line → mute the background → label directly → mark events → add impact indicators → write an insight title → state the next step.
- **Label trick for comparisons**: put the focus bar's label at its far end and the others' at their start, so the eye travels across the gap.
- **Mark estimates explicitly**: an "E" marker, a transparent fill and a dashed outline.
- **Use a waterfall to explain movement** between an opening and closing value. Break the axis only when it's needed to make small changes visible, and mark the break clearly.
- **Write action titles that work without the chart.**
- **When there's no single message** (an infographic), treat every item equally and give side facts lighter visual weight.
- **Context sets the standard.** A scale-bending flourish may be fine in casual social content and unacceptable in a business report.
- Faces and direct, color-matched labels attract the eye and remove the need for a legend.

---

## Key takeaways

1. A visualization exists to communicate. It fails if decoding fails, and a chart on its own isn't a story.
2. Design for perception: position > length > angle > area > volume/curvature > color, using as few tasks as possible. Expect viewers to wander, notice what stands out, remember two or three things, invent relationships and trust conventions.
3. Not everything needs a chart. One value → a sentence or number. Exact values → a table. Patterns → a chart.
4. Match the chart to the purpose. Avoid 3D, pies, radar charts, word clouds, dynamite plots, stacked areas and unnormalized shaded maps.
5. Declutter: maximize data-ink and density within reason, delete everything and add back what's needed, label directly.
6. Use color with purpose: grey + one data color + one highlight, red/green only for meaning, consistent and colorblind-safe.
7. Tell the truth: Lie Factor ≈ 1, bars from zero, visible axis breaks, consistent intervals, no fake dimensions, dashed forecasts, error bars with their method stated.
8. Question the data: causation, bias, comparison, normalization, Simpson's paradox.
9. Context turns information into insight: consult the audience, find the real metric and levers, frame honestly, choose an arc.
10. Title the insight, annotate the why, add a few indicators, summarize briefly and end with next steps.

---

## Checklist

**Before drawing**
- [ ] One message, one audience, one decision or lever
- [ ] Context and the real success metric confirmed with the requester
- [ ] Would a sentence, number or table be better?
- [ ] Purpose identified: time, comparison, relationship, distribution, part-to-whole or spatial
- [ ] Highest-ranked encoding chosen

**Data integrity**
- [ ] No causal claim from correlation alone; hidden variables considered
- [ ] Sample free of selection and attrition bias; *n* known
- [ ] Same denominators; inflation-adjusted; per capita where relevant
- [ ] Subgroups checked
- [ ] Time window not cherry-picked; like-for-like comparisons

**Design**
- [ ] No 3D, shadows, heavy grids, background fills or redundant legends
- [ ] Direct labels, units stated once, horizontal text, measure named
- [ ] One base color plus one highlight; grayscale and colorblind tested
- [ ] Only story-relevant elements shown
- [ ] Annotations explain the why
- [ ] Forecasts dashed; error bar method stated
- [ ] Aspect ratio considered (about 1:1.6, slopes near 45°)

**Visual integrity**
- [ ] Bars and areas start at zero; any break clearly marked
- [ ] Lie Factor ≈ 1; no area or volume icons for 1D data
- [ ] Line range neither flattens nor exaggerates
- [ ] Dual axes don't distort

**Story**
- [ ] Title states the conclusion and passes the 5-second test
- [ ] Numbers compared to a target, peer or past
- [ ] Hero or villain highlighted; every element supports the message
- [ ] Two or three impact indicators
- [ ] Single chart for an insight, dashboard only for an overview
- [ ] Ends with next steps
