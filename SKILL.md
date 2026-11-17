---
name: publication-chart-designer
description: Create, revise, and audit publication-ready research figures for AI, physical science, genuine 3D data, academic comparisons, statistical tests, regression, machine learning, and bioinformatics. Use for complex scientific data, disciplined typography, reproducible Python or R plots, uncertainty, journal sizing, and export review; not decorative dashboards or invented research results.
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

For the eight scientific domains, read the relevant section of [references/domain-atlas.md](references/domain-atlas.md) for specialized encodings and analysis prerequisites. [scripts/render_domain_gallery.py](scripts/render_domain_gallery.py) provides eight runnable two-panel examples using explicit synthetic data and computed results. Adapt them to actual data; they do not replace scientific model validation.

Read [references/chart-selection.md](references/chart-selection.md) when choosing among chart types or when the requested chart could misrepresent the comparison. After choosing a type, read the matching section of [references/chart-playbook.md](references/chart-playbook.md) for production defaults and text limits. Design claims in the playbook are grounded in [references/evidence.md](references/evidence.md).

Prefer position and length over area, angle, or volume. Use a single shared axis when panels invite comparison. For bar and area charts, start at zero unless a zoom is essential and unmistakably signaled. Use log scales only when ratios are meaningful.

A useful design pass is:

1. Sketch the groups, observations, baseline, and comparison in grayscale at final physical size.
2. Remove marks that do not support the stated claim.
3. Add only the labels and color, shape, or line-style distinctions that reduce search time; do not label every mark.

Apply a clarity budget before adding detail:

- Give each panel a clear analytical role. For many estimates, use grouped rows, adequate height, and coordinated summary/detail panels; do not impose an arbitrary row ceiling that hides useful evidence.
- Do not duplicate the axis with a per-row value column unless exact values are essential.
- State constant sample sizes once, in a subtitle, caption, or panel note rather than repeating them on every row.
- Use a forest or coefficient plot for many estimates that require precision comparisons. Use a clean bar chart or small multiples when a few means need to be understood quickly.
- Keep the main grouping and reading order visible at thumbnail size. Recompose the hierarchy when needed; complexity is welcome when it is organized and scientifically useful.
- Apply at most two emphasis devices, such as color and direct labels. More emphasis everywhere removes hierarchy.

Treat the figure and caption as one unit. Put sample size, exclusion rules, transformations, interval definitions, and model details in the caption unless the figure must stand alone. Keep titles, panel names, axes, and genuinely decoding annotations in the plot itself.

## 4. Build at Final Size

Read [references/typography.md](references/typography.md) for weight, upright/italic scientific notation, and final-size hierarchy. Treat text roles deliberately; do not italicize an entire axis label to style a variable. `role_text()` supports consistent prose annotations, and mathtext handles mixed scientific notation.

Use the editorial composition in [references/flat-layout.md](references/flat-layout.md) before drawing. The goal is distinctive, premium visual order rather than minimalism: rich evidence, disciplined typography, modular alignment, deliberate proportions, shared legends and a coherent hierarchy. Start with [scripts/render_domain_gallery.py](scripts/render_domain_gallery.py) for complex scientific plates; the smaller [scripts/render_gallery.py](scripts/render_gallery.py) remains a basic example. Give equal comparisons equal geometry, and use deliberate unequal panels for overview/detail. A new palette alone is not a design improvement.

For Matplotlib, copy the complete [assets/](assets/) directory and [scripts/figure_kit.py](scripts/figure_kit.py) into the project. The assets include the publication style, IBM Plex Sans/Serif fonts under the SIL Open Font License, and the categorical/continuous color definitions.

Initialize a portable visual system with:

```python
from figure_kit import use_publication_style, publication_figure, save_publication_figure

use_publication_style(
    "assets/publication.mplstyle",
    palette="editorial",
    typography="sans",
    context="paper",  # screen / slide / poster use larger type
    language="en",  # zh detects an installed Chinese font
)
fig, ax = publication_figure(width="single", ratio=0.64)
ax.plot(x, y, color="#1F3A5F")
save_publication_figure(fig, "figures/figure_02_policy_effects")
```

Use `palette="editorial"` as the refined default, `palette="accessible"` for the Okabe-Ito set, `palette="ocean"` for cool descriptive figures, or `palette="grayscale"` for print-first work. Use `colormap("sequential")` and `colormap("diverging")` for continuous data.

Read [references/visual-system.md](references/visual-system.md) when choosing typography, categorical colors, continuous scales, or a distinctive visual tone. Read [references/journal-profiles.md](references/journal-profiles.md) when matching a venue or page width.

For chart-specific Matplotlib patterns, read [references/matplotlib-recipes.md](references/matplotlib-recipes.md). For R, preserve the same statistical and perceptual decisions with `ggplot2`; do not force Matplotlib dimensions, annotations, or theme behavior onto an R plot.

Use these defaults unless the venue overrides them:

- single-column width around 3.3–3.5 inches; full-width around 6.5–7.2 inches;
- IBM Plex Sans for modern multipanel work or IBM Plex Serif for traditional papers;
- labels and ticks at final print size, commonly 7–9 pt;
- thin axes and minimal grid lines;
- a restrained categorical palette plus shape, line-style, or direct-label redundancy;
- perceptually ordered sequential or meaningful diverging scales for continuous data;
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

Also inspect a thumbnail: grouping and reading order should remain visible, panel geometry should be balanced, and recurring title baselines should align. Inspect the full-size output for detailed evidence. Use `refine_axes(ax, grid="y")` after numeric plotting for quiet grids. Avoid decorative shadows, categorical gradients, fake 3D extrusion, pill bars, and dashboard card frames. Genuine 3D surfaces and trajectories are supported with matched projections. Heatmap cell geometry should reflect the matrix and annotation tracks; dense expression matrices may use rectangular cells.

Run the automated export check after rendering:

```bash
python scripts/audit_figure.py figures/figure_02_policy_effects.pdf figures/figure_02_policy_effects.png
python scripts/palette_audit.py --palette editorial
```

The checks cover basic file, font, and color-separation properties, not statistical correctness or visual legibility. Always inspect the rendered image as well.

## Deliver

Use a stable stem that identifies the figure in context, such as `figure_02_policy_effects.py`, `.pdf`, `.svg`, and `.png`. Keep the plotting script beside the outputs.

Provide:

- the figure in the requested format and physical size;
- reproducible code with paths or data-loading instructions;
- a caption stating what is shown, the sample, the uncertainty representation, and the bounded takeaway;
- alt text describing the visual structure and finding without repeating the full caption;
- a short note on assumptions, exclusions, or unresolved data issues.
