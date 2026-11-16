# Journal and Layout Profiles

Use these approximate widths as starting points, then verify the current author guidelines for the target venue. Journals revise specifications; a bundled profile is not a guarantee of compliance.

| Profile | Width | Typical use |
| --- | ---: | --- |
| `single` | 3.4 in / 86 mm | Generic single-column manuscript figure |
| `1.5` | 4.8 in / 122 mm | Intermediate or 1.5-column layout |
| `double` | 7.0 in / 178 mm | Generic full-width manuscript figure |
| `nature-single` | 3.50 in / 89 mm | Nature-family single-column figure |
| `nature-double` | 7.20 in / 183 mm | Nature-family full-width figure |
| `science-single` | 2.17 in / 55 mm | Science one-column figure |
| `science-double` | 4.72 in / 120 mm | Science two-column figure |
| `science-triple` | 7.20 in / 183 mm | Science full-width figure |
| `ieee-single` | 3.50 in / 89 mm | IEEE single-column figure |
| `ieee-double` | 7.16 in / 182 mm | IEEE full-width figure |
| `plos-full` | 7.50 in / 190 mm | PLOS maximum figure width |
| `apa-page` | 6.50 in / 165 mm | APA-style page with 1-inch margins |

```python
fig, ax = publication_figure(width="nature-double", ratio=0.38)
```

Choose height from the content, not from a journal logo or house template. Dense multipanel figures often use a height-to-width ratio around 0.25–0.45; single plots commonly use 0.55–0.75.

## Typography Compatibility

- Sans profiles are the safest default for small labels and multipanel figures.
- Serif profiles suit traditional working papers and some social-science and humanities journals.
- Do not use a serif face that becomes visually heavier than the surrounding manuscript at final size.
- Preserve the user's document font when the figure will sit inside a thesis or report and the venue does not require a different figure face.
- Check whether the venue requires editable text, embedded fonts, minimum point size, or a raster-only submission.

## Layout Checks

- Single-column figures should not contain a legend that consumes more than roughly one quarter of the plotting area.
- Full-width figures should exploit horizontal comparison or small multiples rather than merely enlarging a single-column plot.
- Keep panel labels outside the data region.
- Respect a final-size height limit rather than reducing all text uniformly.
- Render at the final width before evaluating label collisions.
