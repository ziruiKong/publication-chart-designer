# Scientific typography: weight and upright/italic roles

Use the destination journal's notation guide when it specifies a convention.
The defaults below distinguish semantic roles rather than decorate text.

| Role | Default weight/style | Size relative to body |
| --- | --- | --- |
| Figure heading | Semibold, upright | +2 to +3 pt |
| Panel letter | Semibold, upright | +1 pt |
| Panel heading | Semibold, upright | +1 pt |
| Axis label / legend title | Regular, upright prose | Body |
| Tick / legend entry / annotation | Regular, upright prose | Body −1 pt |
| Secondary note | Regular, upright, muted but readable | Body −1 pt |
| Scalar variable | Regular italic inside mathtext | Same as surrounding text |
| Unit / numeral / mathematical operator | Regular upright | Same as surrounding text |
| Vector / matrix | Bold mathematical symbol when field convention requires it | Same as surrounding text |

Avoid whole-figure bold, lightweight tiny ticks, faux italic, all-italic axes,
or mixing serif/sans families without a semantic reason. Use bundled real
Regular, Italic, SemiBold, and Bold faces. Do not use bold italic when that face
is unavailable; choose a real supported mathematical font or a regular italic
variable instead. Chinese prose stays upright; italic Latin variables belong
in the math segment only. Do not expand bold Chinese into every label.

Examples in Matplotlib:

```python
ax.set_xlabel(r"Time, $t$ (s)")
ax.set_ylabel(r"Velocity, $v$ ($\mathrm{m\,s^{-1}}$)")
ax.set_title("Model diagnostics", fontweight="semibold", fontstyle="normal")
role_text(ax, 0.03, 0.96, r"$n$ = 600; $R^2$ = 0.81", role="annotation")
ax.set_ylabel(r"$-\log_{10}(q)$")
```

Scalar variables such as x, t, n, p, q, and R in R² are typically italic in
mathematical/statistical contexts; log, exp, sin, min, and max are upright
operators. Descriptive subscripts are upright (`$x_{\mathrm{control}}$`),
variable indices italic (`$x_i$`). CI, SD, SE, AUC, RNA, model names, gene
identifiers used as labels, and units remain upright by default. Italic gene
symbols depend on organism nomenclature; distinguish genes from proteins and
follow that discipline's guide. Do not blindly italicize all Greek letters or
all statistical abbreviations; conventions differ between publishers.

Keep size context coherent: paper 8 pt, screen 11 pt, slide 14 pt, poster 18 pt
are starting points. The venue minimum wins. Check a normal-size render, PDF
font embedding, minus signs, superscripts, math glyphs, Chinese, and regular
versus semibold distinction. A visually balanced title must not dwarf the data.

Unit typography reference: [BIPM SI Brochure](https://www.bipm.org/en/publications/si-brochure).
Use this for SI unit/quantity conventions; publisher-specific statistical and
biological notation still needs its own guide.
