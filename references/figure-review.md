# Figure Review

Use this checklist before and after rendering. It supplements, rather than replaces, inspection of the exported figure.

## Data and Claim

- The figure answers one question that can be stated in a sentence.
- The observation unit and denominator are known.
- Every plotted value comes from the supplied data or a stated calculation.
- Missing observations, exclusions, weights, transformations, and model adjustments are documented when they affect interpretation.
- The graphical comparison matches the statistical comparison.
- The caption does not make a stronger causal or predictive claim than the design supports.

## Uncertainty

- Every interval has a precise definition: confidence, credible, standard error, standard deviation, range, quantile, or another stated interval.
- The interval is appropriate to the quantity plotted.
- Sample size or precision is visible where readers need it.
- Error bars are not shown for categories that contain only one observation.
- Significance marks, if used, correspond to a named test and are not the only encoding of the result.
- Overlapping intervals are not described as proof of no difference.

## Marks and Axes

- Bars and filled areas begin at zero unless a clearly marked zoom is essential.
- Axis limits do not clip legitimate values or hide the baseline in a misleading way.
- Tick intervals are readable and consistent across comparable panels.
- Log scales are used only for meaningful ratios and are visibly labeled.
- A fitted line is distinguished from observed data and is not presented as causal evidence without a causal design.
- Smoothed trends do not replace raw observations without disclosure.
- Area, angle, and bubble-size encodings have a legend or direct scale when readers must decode magnitude.

## Color and Accessibility

- Color is not the only distinction among categories.
- The palette remains understandable in grayscale and for common color-vision deficiencies.
- Text and marks have sufficient contrast against their backgrounds.
- Sequential scales use perceptually ordered colors; diverging scales have a meaningful midpoint.
- Rainbow scales are avoided for ordered continuous data.
- The figure works in light and dark viewing contexts when the destination requires both.

## Composition and Type

- The figure was composed near its final physical width.
- The smallest tick, legend, and annotation text remains legible at final size.
- Panel labels use one style and are positioned consistently.
- Direct labels replace legends where they reduce search effort.
- Titles, subtitles, and annotations do not repeat the caption unnecessarily.
- Decimal precision is consistent and no more precise than the measurement supports.
- Units appear in axis labels, tick labels, or direct annotations.
- The figure does not duplicate the axis with a full column of values unless exact values are essential.
- Constant sample sizes are stated once rather than repeated in every category.
- At most two emphasis devices dominate: for example color plus direct labels, not color, arrows, boxes, and bold text together.

## Export

- PDF/SVG is used for vector work when the venue accepts it.
- Raster output is at least 300 dpi at final physical size.
- Fonts are embedded or preserved according to the output format.
- No labels are clipped by `bbox_inches="tight"` or by manual figure bounds.
- The PDF has the expected page count and no transparent background unless requested.
- The source data and plotting script travel with the figure.

## Final Visual Test

1. Open the exported file at its intended physical size, not in a zoomed editor.
2. Read the figure in grayscale.
3. Read it without the caption.
4. Compare it with the underlying table or raw data for at least one plotted value.
5. Check one interval, one extreme observation, and one annotation back to the source.
6. Confirm the caption and alt text describe what is actually visible.
7. Shrink the figure enough that the main comparison should remain obvious. If it disappears, the design is too dense.

Report unresolved issues instead of concealing them with styling.
