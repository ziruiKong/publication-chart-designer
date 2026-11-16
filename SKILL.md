---
name: publication-chart-designer
description: Design and implement publication-ready charts for academic papers, theses, and research reports, including chart choice, reproducible Python or R code, journal styling, and export checks. Use when a research figure must be accurate, accessible, and submission-ready; not for dashboards, decorative infographics, or charts whose underlying data would be invented.
---

# Publication Chart Designer

Create figures that communicate one defensible research finding without visual distortion. Unless the user asks only for advice, deliver the figure, the code that reproduces it, a concise caption, and alt text.

## Establish the Figure Contract

Before styling, identify:

- The claim or comparison the figure must support.
- The data source, variables, units, and sample size.
- The target venue, column width, file format, and any journal style rules.
- Whether the chart is destined for a paper, thesis, slide, poster, or web supplement.

Use actual data. Never fabricate values, uncertainty, significance, or trends. If source data are unavailable, either request them or clearly label a schematic as a design mockup rather than a result.

## Choose the Chart From the Statistical Task

- Read [references/chart-selection.md](references/chart-selection.md) when choosing among chart types or when the requested chart could misrepresent the comparison.
- Prefer direct comparisons, position, and length over area, angle, or volume.
- Show distributions when central tendencies could hide heterogeneity.
- Show uncertainty whenever the figure supports an inferential claim.
- Use a single axis unless a dual-axis display is unavoidable and explicitly justified.

## Apply Publication Style

Start from [assets/publication.mplstyle](assets/publication.mplstyle) for Matplotlib projects. Copy the style file into the working project and load it with `plt.style.use(...)` so the output remains reproducible.

Use these defaults unless the venue overrides them:

- Single-column width around 3.3–3.5 inches; full-width around 6.5–7.2 inches.
- Sans-serif type for labels and ticks, typically 7–9 pt at final print size.
- Thin axes, minimal grid lines, and no chart junk or heavy shadows.
- Colorblind-safe colors with distinct markers, line styles, or direct labels so meaning survives grayscale reproduction.
- Vector output such as PDF or SVG for manuscripts; 300–600 dpi PNG only when a raster format is required.
- Embed fonts and avoid text smaller than the journal’s minimum.

For R users, translate the same decisions to `ggplot2`; do not change the statistical message merely to fit a template.

## Build and Check

1. Compute summaries and uncertainty in code rather than typing values into the plotting call.
2. Label axes with variables and units; keep panel labels consistent.
3. Make legends unnecessary when direct labels are clearer.
4. Render at final dimensions and inspect the exported image, not only the plotting code.
5. Check clipping, overlapping labels, unreadable grayscale encoding, inconsistent decimals, and accidental visual exaggeration.
6. Verify that every value and annotation traces back to the supplied data.

Save the plotting script beside the generated figure and use a stable stem such as `figure_02_policy_effects.py`, `.pdf`, `.svg`, and `.png`.

## Deliver

Provide:

- The figure in the requested format and size.
- Reproducible code with paths or data-loading instructions.
- A caption that states what is shown, the sample, the uncertainty representation, and the takeaway.
- Alt text that describes the visual structure and the finding without repeating the full caption.
- A short note on any assumption, excluded observation, or unresolved data issue.
