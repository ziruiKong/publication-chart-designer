# Chart Playbook

Use this after identifying the analytical task and before writing plotting
code. Evidence keys refer to [evidence.md](evidence.md).

## Common Text Budget

Treat the plotted image and its caption as one communication unit. The plot
should carry the comparison; the caption should carry methods and explanation.

In the figure itself:

- use one short title if the destination requires an embedded title;
- use panel titles of roughly one to four words;
- label axes with quantity and unit;
- place sample size, interval definition, exclusions, transformations, and
  model details once in the caption unless the figure must stand alone;
- avoid a value printed on every mark when a readable axis already communicates
  the quantity;
- limit annotations to the threshold, event, or contrast needed to decode the
  result;
- use direct labels to replace a legend, not to repeat the axis.

For a standalone poster or slide, add at most one short explanatory subtitle.
For a journal figure, prefer the caption. [E3, E5]

## Categorical Comparison: Bar, Dot, or Small Multiples

Use when a few groups differ on one quantity.

Default:

- horizontal dot plot when exact values and ranking dominate;
- bars only when zero is meaningful and length carries the message;
- one consistent color unless category identity is essential;
- direct category labels instead of a separate legend;
- uncertainty interval when the comparison is inferential;
- small multiples when two dimensions compete in one panel.

Avoid:

- 3D bars, cylinders, shadows, and decorative gradients;
- a second color layer that repeats labels already on the axis;
- labeling every bar when the axis is sufficient;
- more than about 8–10 bars before switching to a dot plot or small multiples.

Evidence: position and length are stronger encodings than area or volume [E1,
E2]; global comparisons are fast but subset switching taxes working memory [E3];
small multiples make conditional comparisons easier [E4].

## Distribution

Use when spread, skew, clusters, outliers, or subgroup structure matters.

Default:

- show raw observations when the sample is small;
- combine points with a compact box, interval, or density only if each layer
  answers a different question;
- use deterministic jitter and state whether points overlap;
- label center and spread precisely in the caption;
- use violin or density only when there are enough observations for a stable
  estimate.

Avoid:

- mean bars with standard-error whiskers as the only view of a small sample;
- violin plots that imply smooth density from very few observations;
- box plots when the median and quartiles are not the quantities of interest.

Evidence: summary bars can conceal distributions and paired structure [E6];
raincloud-style displays can jointly show raw data, distribution, and summary
with limited redundancy [E7].

## Time Trend

Use when a quantity evolves over an ordered continuous dimension.

Default:

- use a continuous x-axis with meaningful time intervals;
- direct-label series at or near the line ends;
- show raw observations when periods are few;
- use a confidence band for model uncertainty and distinguish it from observed
  spread;
- annotate only major events or method breaks;
- share scales across comparable panels.

Avoid:

- connecting unordered categories;
- smooth lines that hide irregular observations without disclosure;
- dual y-axes unless no defensible alternative exists;
- a legend when direct series labels fit.

Evidence: perceptual accuracy depends on the encoding [E1]; attention and
working memory should be guided rather than tested [E3]; method and uncertainty
details belong in the caption [E5].

## Forest or Estimation Plot

Use when many effects or model coefficients require comparison on a shared
scale.

Default:

- plot point estimates with interval lines;
- show a zero or meaningful reference line;
- order rows by substantive grouping, time, or effect size;
- use a distinct mark for an overall estimate;
- include interval definition in the caption;
- include a value column only when exact point estimates are essential and the
  figure needs table-like reading.

Avoid:

- forest plots for three or four means that are easier to read as a simple
  small-multiple comparison;
- p-value stars as the focus;
- arbitrary significance sorting;
- repeating both interval lines and a full table of values by default.

Evidence: forest plots are a convention for many estimates and uncertainty
[E8]; estimation graphics shift attention toward effect size and precision
[E9].

## Scatter and Association

Use when the relationship between two continuous variables matters.

Default:

- show raw observations;
- reduce overplotting with small marks, transparency, binning, or contours;
- state the fitted model and interval when a trend line is shown;
- use shared scales when panels are compared;
- label unusual observations only when they are substantively relevant.

Avoid:

- causal language in an observational association;
- dense opaque points that hide sample size;
- a fit line with no method or uncertainty;
- a correlation annotation replacing the actual pattern.

Evidence: raw observations reveal features hidden by summaries [E6]; visual
encodings and attention management affect pattern extraction [E1, E3].

## Composition

Use when parts form a whole.

Default:

- use stacked or grouped bars when the number of categories is small;
- sort segments in a stable substantive order;
- use direct labels for two to four segments;
- use a dot plot when exact comparison matters more than seeing the whole.

Avoid:

- pie or donut charts beyond a few categories;
- exploded slices or 3D perspective;
- comparing many segment percentages without aligned baselines.

Evidence: position and length are more accurate than angle and area [E1];
simplicity and message clarity should outweigh decoration [E5].

## Choropleth and Spatial Comparison

Use for rates or normalized measures across geography.

Default:

- map rates, proportions, or residuals rather than raw counts;
- use a sequential scale for magnitude and a diverging scale only for a
  meaningful midpoint;
- state class breaks or continuous scale limits;
- include missing-data and small-denominator information;
- use a compact legend and avoid too many bins.

Avoid:

- rainbow or red–green scales;
- raw counts for unequal population sizes;
- color changes that imply boundaries absent from the data;
- heavy borders and labels that dominate the pattern.

Evidence: perceptual color maps preserve data order and remain accessible
[E10, E11]; map color schemes must match data type [E12].

## Paired Change: Slope or Dumbbell

Use when the same unit is measured under two or more conditions.

Default:

- connect paired observations or show within-unit differences;
- emphasize direction and magnitude of change;
- show all units when the sample is small;
- direct-label conditions at the endpoints.

Avoid:

- independent-group bars for paired data;
- plotting only group means when consistency of change matters;
- connecting units that are not actually paired.

Evidence: paired data need displays that preserve the unit-level structure
[E6].

## Ranking

Use when ordering is the message.

Default:

- use a sorted dot plot with direct labels;
- show uncertainty where estimates are model-based;
- preserve the substantive order after sorting;
- highlight one or a small number of ranks only if the claim concerns them.

Avoid:

- dense rank tables;
- color gradients that imply an interval scale across ranks;
- unstable rankings presented without uncertainty.

Evidence: position is an accurate comparison channel [E1]; precision and effect
size should remain visible [E9].

## Repeated Measures

Use when units are measured repeatedly across time or conditions.

Default:

- show individual trajectories in light lines when the sample is manageable;
- highlight group summaries or selected exemplars without hiding all traces;
- use small multiples when trajectories belong to distinct groups;
- state smoothing and missing-data rules.

Avoid:

- bars that erase within-unit change [E6];
- spaghetti plots with opaque overplotting and no summary;
- separate panels that break the paired trajectory.

Evidence: hide-the-data plots can reverse interpretation [E6]; small multiples
support conditional comparison [E4].

## Event Study

Use for dynamic treatment effects around an event or policy.

Default:

- plot coefficients over event time;
- show a zero reference line and a visibly defined reference period;
- show confidence intervals;
- preserve meaningful event-time spacing;
- separate estimation details from the plotted effect.

Avoid:

- two before/after bars that erase dynamics;
- hiding pre-treatment coefficients;
- treating a flat post-period as causal evidence without discussing assumptions.

Evidence: event-study visualization should expose dynamic effects and the
assumptions needed for identification [E14].

## Heatmap and Matrix

Use for a dense two-dimensional pattern.

Default:

- use a perceptually ordered sequential map for magnitude;
- use diverging color only around a meaningful midpoint;
- sort rows and columns when order is not intrinsic;
- annotate selected cells, not every cell;
- state units and scale limits.

Avoid:

- rainbow maps and red–green contrast;
- full numeric tables printed over every cell;
- unlabeled dendrograms or reorderings that conceal the substantive order.

Evidence: scientific color maps and CVD-aware design [E10, E11].

## Model Diagnostics

Use residual, calibration, influence, and fitted-versus-observed plots to
evaluate a model rather than to sell it.

Default:

- show the reference pattern expected under a correct model;
- use small multiples when several diagnostics share a scale;
- annotate influential observations only when decision-relevant;
- state smoothing and thresholds.

Avoid:

- a “good fit” line with no residual view;
- overplotting that hides model failure;
- diagnostic annotations that crowd out the pattern.

Evidence: visualization should expose data structure rather than conceal it
[E6], and the plot must be designed around the inferential question [E5].

## Small Multiples

Use when one chart would require more than two competing dimensions.

Default:

- one panel per meaningful subset;
- shared scales unless scale differences are the message;
- aligned rows and columns;
- concise panel titles;
- one shared legend or direct labels where possible.

Avoid:

- repeating a full legend in every panel;
- panel-specific scales that invite false comparison;
- treating small multiples as a place to repeat every annotation.

Evidence: trellis displays support conditional comparison [E4]; shared visual
structure reduces working-memory load [E3].
