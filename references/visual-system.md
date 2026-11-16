# Visual System

Use this reference when the user asks for a polished, distinctive, or journal-like look, or when color and typography choices materially affect interpretation.

## Typography

The skill bundles IBM Plex Sans and IBM Plex Serif under the SIL Open Font License. Register the bundled font files before rendering; `use_publication_style()` does this automatically.

Use one of two typographic profiles:

| Profile | Best for | Family | Behavior |
| --- | --- | --- | --- |
| Modern sans | Most journals, reports, slides, multipanel figures | IBM Plex Sans | Neutral, compact, highly legible at small sizes |
| Scholarly serif | Working papers, humanities, traditional social-science documents | IBM Plex Serif | More editorial and book-like while retaining screen clarity |

```python
from figure_kit import set_font_family, set_typography, use_publication_style

use_publication_style(typography="sans")
# Or: set_typography("serif")

# For mixed Latin and CJK labels, keep an explicit fallback chain:
set_font_family(
    ["IBM Plex Sans", "Noto Sans CJK SC", "Microsoft YaHei", "PingFang SC"],
    base_size=8,
)
```

Use 8 pt as a starting point, 7 pt for dense full-width panels, and 9–10 pt when the figure will be viewed primarily on screen. Adjust to the final physical width and venue instructions rather than scaling a large draft down.

Typography rules:

- Use one family within a figure unless a second face carries a specific distinction.
- Use weight, spacing, and alignment before introducing extra colors.
- Keep tick labels, legends, and annotations within 1–2 pt of each other.
- Use semibold for emphasis; avoid heavy bold except panel labels and very short headings.
- Use sentence case for titles and labels.
- Keep decimal precision consistent and omit redundant leading zeros only when the venue does.
- Use real italics for variables and statistical notation; do not slant text manually.
- For Chinese, Japanese, or Korean labels, set an installed CJK family explicitly. IBM Plex Sans does not cover all CJK glyphs; Noto Sans CJK SC, Source Han Sans SC, and PingFang SC are suitable fallbacks.

## Categorical Color

Start with one palette, then add shape, marker, line style, or direct labels.

| Palette | Character | Recommended use |
| --- | --- | --- |
| `editorial` | Deep navy, terracotta, sage, plum, ochre, slate | Default for a refined paper figure with a limited number of series |
| `accessible` | Okabe-Ito colorblind-safe set | Maximum accessibility, methods figures, categories where hue does most work |
| `ocean` | Teal and sand with restrained warmth | Environmental, geographic, longitudinal, and descriptive figures |
| `grayscale` | Ordered neutral inks | Print-first figures, annotations, or a deliberate monochrome system |

```python
from figure_kit import palette_colors, set_palette

colors = set_palette("editorial")
highlight = palette_colors("editorial")[1]
```

Rules:

- Use about 4–6 categories before switching to small multiples.
- Keep the same color meaning across panels.
- Use the strongest contrast for the comparison the figure is making.
- Assign neutral grays to context, baselines, and secondary information.
- Use saturated colors for data, not backgrounds, frames, or decoration.
- Do not rely on hue alone. Pair color with shape, line style, position, or direct labels.
- Do not use ordered colors for unordered categories or categorical colors for an ordered scale.

## Continuous Color

Use `colormap("sequential")` for ordered magnitude and `colormap("diverging")` only when a meaningful midpoint exists.

```python
from figure_kit import colormap

sequential = colormap("sequential")
diverging = colormap("diverging")
```

- State the scale definition and units in the colorbar.
- Use a diverging map only around a meaningful zero, parity point, or policy threshold.
- Do not use rainbow or jet for ordered data.
- Do not let a colorbar create more precision than the measure supports.
- Use annotated levels or contours when readers need exact thresholds.

## Contrast and Ordering

Test the figure against white. Dark navy, terracotta, deep teal, and near-black remain legible; pale colors should be used for fills, uncertainty bands, or secondary marks rather than one-pixel lines and labels.

Order categorical colors deliberately:

1. primary finding or treatment;
2. comparison group;
3. secondary contrasts;
4. neutral context.

Do not choose colors merely to maximize difference; the palette should still feel like one designed system.

## Audit

Run the palette audit after changing colors:

```bash
python scripts/palette_audit.py --palette all
```

Use the report as a diagnostic. A palette can pass separation checks and still fail because of poor ordering, too many categories, low contrast, or redundant encoding. Inspect the figure in grayscale and at final size.
