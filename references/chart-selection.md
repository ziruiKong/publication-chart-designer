# Chart Selection Guide

Choose a chart from the statistical task, not from decoration. State the comparison in one sentence before reviewing this table.

| Research task | Preferred starting point | Avoid or use cautiously |
| --- | --- | --- |
| Compare a few category values | Horizontal dot plot; bar chart when length is meaningful and zero is meaningful | 3D bars, exploded pies, decorative cylinders, truncated bar charts |
| Compare distributions | Box plot with raw points, strip plot, or another distribution display | Bar-plus-SD when skew, clusters, or multimodality matters |
| Show a trend over time | Line chart with raw observations and direct series labels | Smoothers that hide raw data without disclosure |
| Show uncertainty | Interval plot, error bars, or confidence band | Error bars whose meaning is not defined |
| Show association | Scatter plot, optionally with a clearly described fitted trend | A fitted curve that implies causality without support |
| Show composition | Stacked bar or dot plot when exact comparison matters | Pie charts with many categories |
| Show many group estimates | Forest or coefficient plot | Sorted bars without uncertainty |
| Show geographic variation | Choropleth with a perceptually ordered scale and accessible legend | Rainbow palettes or unclassed rates based on tiny samples |
| Show paired change | Slope or dumbbell plot | Two unrelated bars that obscure within-unit change |
| Show model fit or residuals | Fitted-versus-observed plot or residual diagnostics | A perfect-looking line with no scale, diagnostics, or disclosure |
| Show a ranking | Sorted dot plot with direct labels and uncertainty where available | Rank labels without denominators or precision |
| Show repeated measurements | Spaghetti plot with highlighted summaries, or a within-unit change plot | Independent group bars that erase within-person structure |
| Show event-time effects | Event-study coefficient plot with a reference period | Two before/after bars that hide pre-trends and dynamic effects |

## Selection Questions

1. Is the task comparison, distribution, trend, association, composition, or prediction?
2. Is the observation unit a person, firm, region, period, model, or something else?
3. Does the reader need to compare exact values or perceive an overall pattern?
4. Is there a meaningful zero or reference category?
5. Is uncertainty part of the claim?
6. Are categories few enough for direct labels?
7. Will the encoding survive grayscale and common color-vision deficiencies?

Do not treat a forest plot as the automatic “publication” answer. When a figure
contains only a few group means, a zero-baseline bar chart or small multiples
can communicate faster and still be rigorous. A forest plot earns its density
when readers need to compare many estimates, intervals, or model coefficients.

## Design Rules

- Label the quantity, not the column name.
- Put units in axis labels or directly next to values.
- Prefer a zero baseline for bars and areas unless a justified zoom is essential.
- Use log scales only when the ratio is meaningful and make that choice explicit.
- Show sample size, number of observations, or uncertainty where relevant.
- Use direct labels when they replace a legend without duplicating a readable axis.
- Use no more colors than the comparison requires.
- Use position and length before area, angle, or bubble size.
- Keep shared scales across comparable small multiples.
- Verify category distinctions remain understandable in grayscale and for common color-vision deficiencies.
- Do not claim significance visually unless the underlying test and interval support it.
- Do not encode two meanings with the same visual channel, such as color for both group and outcome level.
- Make missing or excluded data visible when exclusion is decision-relevant.
- Remove direct labels or value columns that merely repeat what a readable axis already shows.
- Put constant sample-size information in one place rather than every row.
- If more than one comparison competes for attention, use small multiples instead of stacking both dimensions into one dense panel.

## Uncertainty

Name the interval before drawing it. Confidence intervals, credible intervals, standard errors, standard deviations, interquartile ranges, and ranges answer different questions.

- Do not add an interval to a category with one observation.
- Do not describe overlapping confidence intervals as proof of no difference.
- Do not use error bars as a substitute for showing a distribution when heterogeneity is the point.
- State whether intervals are marginal, conditional, clustered, weighted, or bootstrapped.
- Use an explanatory caption or panel note for any transformed interval.

## Caption Skeleton

“Figure X shows [quantity] for [sample/comparison] across [dimension]. Points/lines represent [estimates], and [error bars/bands] show [uncertainty definition]. The figure indicates [bounded interpretation].”
