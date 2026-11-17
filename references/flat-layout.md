# Editorial order and flat figure composition

The desired direction is an immediately recognizable, carefully composed scientific
plate: rich information, precise alignment, deliberate typography, disciplined
color relationships, and flat rendering. Minimalism is not the objective.
White canvas, fine neutral axes, and solid data marks support that order. Respect venue
requirements when they differ. The reference project
[academic-plot](https://github.com/mintandkiwi/academic-plot) demonstrates reusable
physical-size profiles, consistent Matplotlib styling, Chinese font detection,
and paired vector/raster export. This skill uses its own implementation and
retains open top/right spines by default rather than copying a four-sided frame.

## Geometry before decoration

Compose the whole plate before polishing individual axes. Establish a modular
grid, a dominant evidence panel, supporting diagnostics, a shared legend zone,
and a concise methods/metadata strip when the format allows it. Use a 2:1 or
3:2 panel-width relationship when analytical importance warrants it. Equal
panels are appropriate for equal comparisons, not a universal constraint.
Align recurring elements to shared anchors; encode grouping with spacing,
short section labels, and fine rules. Avoid generic dashboard cards.

Complexity belongs in meaningful layers: raw observations, summary/uncertainty,
group identity, and diagnostic context. Remove redundancy rather than removing
the evidence. Use density, rasterized point layers, annotation tracks, dendrograms,
and coordinated panels when they make large datasets readable. Stable color
semantics and scale relationships should unify the entire plate.

Reference discovery: [Plottie](https://plottie.art/) lists journal figures such
as stacked distributions, spectral decompositions, bubble matrices, volcano
plates, and genomic tracks. Inspect an accessible example before claiming a
specific visual match; individual detail pages may require browser verification.
Use references for compositional principles, never copy their data or imply
their journal attribution applies to generated demonstration figures.

- Use a modular grid for comparable panels. Start at 3:2 for a single plot;
  allocate height from the number of rows for ranked or interval plots.
- Align plot rectangles, title baselines, units, and recurring legends. Keep
  panel gaps consistent; allow more room for long labels rather than shrinking
  all text. For unequal labels, use GridSpec or subfigures deliberately.
- Keep bar widths near 0.6 of a category interval; use square corners, equal
  group gaps, and one baseline. Never round or taper a quantitative endpoint.
- Use circles for observations, thin straight intervals, and consistent caps.
  Change marker shape only when it encodes a category.
- Start with 4–6 major numeric ticks and a light grid on the measurement axis.
  Dates, log axes, and categorical positions need their own explicit locators.
- Use square heatmap cells when both dimensions are discrete comparable units.
  Rectangular cells are appropriate when a dimension represents time or space.
- Put legends in a reserved strip or empty space; never cover observations.
  Keep direct labels short and check close endpoints for collisions.

## Hierarchy and color

Choose a paper/screen/slide/poster context before drawing. Use the role hierarchy
in [typography.md](typography.md), quiet tick labels, and consistent vocabulary.
Chinese text requires a detected installed CJK font, not merely a font name in
a fallback list. A missing-font warning must be resolved before delivery.

Use a coherent palette with distinct roles: deep anchor color, supporting hues,
and quiet neutral context. Use more colors when the data require distinct groups;
preserve their meanings across panels. Do not assign a different color to each bar
when the category labels already distinguish them. Use continuous gradients
only for continuous measurements. No shadows, bevels, fake 3D extrusion, decorative backgrounds,
gloss, or heavy outlines. Flat does not mean faint: data must stand above the grid.

## Render and judge

Inspect both full-size output and a thumbnail. Check spacing, title alignment,
coherent panel proportions, readable units, unclipped legends, and a visible main comparison.
Fix the composition and render again when any of these fails.

`save_publication_figure()` preserves physical canvas dimensions by default.
Use constrained layout and keep annotations within that canvas. `crop=True`
is available for informal previews; cropping can change journal dimensions.
The gallery uses explicitly labeled synthetic design data, never research results.
