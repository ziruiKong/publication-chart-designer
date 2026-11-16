---
name: publication-chart-designer
description: Create, revise, and audit publication-ready charts for academic papers, theses, and research reports, including chart selection, statistical presentation, reproducible Python or R code, journal styling, and export checks. Use when a research figure must be accurate, accessible, and submission-ready; not for dashboards, decorative infographics, or charts whose underlying data would be invented.
---

# Publication Chart Designer

Create a figure that makes one defensible research finding easier to understand without exaggerating or hiding uncertainty. Unless the user asks only for advice, deliver the rendered figure, reproducible code, a concise caption, and alt text.

## 1. Establish the Figure Contract

Before styling, identify:

- the claim or comparison the figure must support;
- the observation unit, sample size, variables, and units;
- the source of every value, interval, and annotation;
- the target venue and its physical dimensions, font rules, and file format;
- whether the figure is for print, slides, a poster, or a web supplement.

If a detail is missing but not blocking, use a conservative default and state it. Do not silently change the comparison, exclude observations, or convert uncertainty into a stronger claim.

Use actual data. Never fabricate values, uncertainty, significance, trends, or geographic patterns. If source data are unavailable, request them or label a schematic explicitly as a design mockup rather than a result.

## 2. Audit the Data and Inference

Resolve these items before choosing a visual encoding:

- denominator and missing-data handling;
- exclusions, transformations, weights, and model adjustments;
- whether intervals are confidence intervals, credible intervals, standard errors, standard deviations, ranges, or quantiles;
- whether annotations and labels were computed from the same data shown in the figure;
- whether a fitted line is descriptive or supports a causal interpretation.

Compute summaries and uncertainty in code rather than typing plotted values into the chart. State the interval definition in the caption or panel note. Do not use asterisks or color alone to imply significance.

For a detailed preflight review, read [references/figure-review.md](references/figure-review.md).

## 3. Choose the Visual Encoding

Read [references/chart-selection.md](references/chart-selection.md) when choosing among chart types or when the requested chart could misrepresent the comparison.

Prefer position and length over area, angle, or volume. Use a single shared axis when panels invite comparison. For bar and area charts, start at zero unless a zoom is essential and unmistakably signaled. Use log scales only when ratios are meaningful.

A useful design pass is:

1. Sketch the groups, observations, baseline, and comparison in grayscale at final physical size.
2. Remove marks that do not support the stated claim.
3. Add direct labels and the minimum color, shape, or line-style distinctions needed.

## 4. Build at Final Size

For Matplotlib, start from [assets/publication.mplstyle](assets/publication.mplstyle). Locate it relative to this skill, copy it into the project, and load it explicitly so the script remains portable.

Copy [scripts/figure_kit.py](scripts/figure_kit.py) and the style file into the analysis project when delivering reusable code. Use the helper for common final-size and export operations:

```python
from figure_kit import use_publication_style, publication_figure, save_publication_figure

use_publication_style("publication.mplstyle")
fig, ax = publication_figure(width="single", ratio=0.64)
ax.plot(x, y, color="#0072B2")
save_publication_figure(fig, "figures/figure_02_policy_effects")
```

For chart-specific Matplotlib patterns, read [references/matplotlib-recipes.md](references/matplotlib-recipes.md). For R, preserve the same decisions with `ggplot2`; do not force Matplotlib dimensions, annotations, or theme behavior onto an R plot.

Use these defaults unless the venue overrides them:

- single-column width around 3.3–3.5 inches; full-width around 6.5–7.2 inches;
- sans-serif labels and ticks at final print size, commonly 7–9 pt;
- thin axes and minimal grid lines;
- colorblind-safe colors plus shape, line-style, or direct-label redundancy;
- PDF or SVG for manuscripts; 300–600 dpi PNG only when raster output is required;
- embedded fonts and no text below the venue minimum.

## 5. Review the Rendered Figure

Render at the intended physical dimensions and inspect the actual output. Check:

- the stated claim is visible without reading the surrounding paper;
- axes, units, denominator, and uncertainty definition are explicit;
- labels do not collide, clip, or shrink below the intended size;
- category distinctions survive grayscale and common color-vision deficiencies;
- zero baselines, log scales, smoothing, and fitted curves do not imply more than the data support;
- panels are ordered and labelled consistently;
- the figure remains legible when viewed at 100% print size.

Run the automated export check after rendering:

```bash
python scripts/audit_figure.py figures/figure_02_policy_effects.pdf figures/figure_02_policy_effects.png
```

The check covers basic file and font properties, not statistical correctness or visual legibility. Always inspect the rendered image as well.

## Deliver

Use a stable stem that identifies the figure in context, such as `figure_02_policy_effects.py`, `.pdf`, `.svg`, and `.png`. Keep the plotting script beside the outputs.

Provide:

- the figure in the requested format and physical size;
- reproducible code with paths or data-loading instructions;
- a caption stating what is shown, the sample, the uncertainty representation, and the bounded takeaway;
- alt text describing the visual structure and finding without repeating the full caption;
- a short note on assumptions, exclusions, or unresolved data issues.
