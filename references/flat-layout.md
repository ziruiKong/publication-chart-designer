# Flat, orderly figure composition

The default direction is intuitive, balanced, and flat: white canvas, dark text,
fine neutral axes, solid data marks, and one restrained accent. Respect venue
requirements when they differ. The reference project
[academic-plot](https://github.com/mintandkiwi/academic-plot) demonstrates reusable
physical-size profiles, consistent Matplotlib styling, Chinese font detection,
and paired vector/raster export. This skill uses its own implementation and
retains open top/right spines by default rather than copying a four-sided frame.

## Geometry before decoration

- Use a rectangular grid for comparable panels. Start at 3:2 for a single plot;
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

Choose a paper/screen/slide/poster context before drawing. Keep one font family,
one short title, quiet tick labels, and a consistent sentence-case vocabulary.
Chinese text requires a detected installed CJK font, not merely a font name in
a fallback list. A missing-font warning must be resolved before delivery.

Use navy for the main series and muted neutral marks for context. Add terracotta
only for a meaningful comparison. Do not assign a different color to each bar
when the category labels already distinguish them. Use continuous gradients
only for continuous measurements. No shadows, bevels, 3D, decorative backgrounds,
gloss, or heavy outlines. Flat does not mean faint: data must stand above the grid.

## Render and judge

Inspect both full-size output and a thumbnail. Check spacing, title alignment,
equal panel boxes, readable units, unclipped legends, and a visible main comparison.
Fix the composition and render again when any of these fails.

`save_publication_figure()` preserves physical canvas dimensions by default.
Use constrained layout and keep annotations within that canvas. `crop=True`
is available for informal previews; cropping can change journal dimensions.
The gallery uses explicitly labeled synthetic design data, never research results.
