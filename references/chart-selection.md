# Chart Selection Guide

Choose a chart from the statistical task, not from decoration.

| Research task | Preferred starting point | Avoid when |
| --- | --- | --- |
| Compare a few category values | Horizontal dot plot or bar chart with a zero baseline | 3D bars, exploded pies, decorative cylinders |
| Compare distributions | Box plot with points, violin plot, or raincloud plot | Bar-plus-SD when skew or multimodality matters |
| Show a trend over time | Line chart with direct series labels | Smoothed lines that hide raw observations without disclosure |
| Show uncertainty | Error bars, confidence bands, or interval plots | Error bars without stating what the interval represents |
| Show association | Scatter plot, optionally with a clearly labeled fitted trend | A fitted curve that implies causality without support |
| Show composition | Stacked bar or dot plot when exact comparison matters | Pie charts with many categories |
| Show many group estimates | Forest or coefficient plot | Sorted bars without uncertainty |
| Show geographic variation | Choropleth with a perceptually ordered scale and accessible legend | Rainbow palettes or unclassed rates based on tiny samples |
| Show paired change | Slope or dumbbell plot | Two unrelated bars that obscure within-unit change |

## Design Rules

- Label the quantity, not the column name.
- Put units in axis labels or directly next to values.
- Prefer a zero baseline for bars and areas unless a justified zoom is essential.
- Use log scales only when the ratio is meaningful and make that choice explicit.
- Show sample size, number of observations, or uncertainty where relevant.
- Use direct labels before adding a legend.
- Use no more colors than the comparison requires.
- Verify category distinctions remain understandable in grayscale and for common color-vision deficiencies.
- Do not claim significance visually unless the underlying test and interval support it.

## Caption Skeleton

“Figure X shows [quantity] for [sample/comparison] across [dimension]. Points/lines represent [estimates], and [error bars/bands] show [uncertainty definition]. The figure indicates [bounded interpretation].”
