# Publication Chart Designer

A Codex skill for creating, revising, and auditing accurate, accessible charts for academic papers, theses, and research reports.

The skill turns a research claim into a defensible visual encoding, then carries it through code, final-size typography, uncertainty, captions, alt text, and export review.

It includes:

- a figure contract and data/inference audit;
- chart-selection guidance;
- a Matplotlib publication style and reusable figure helpers;
- bundled IBM Plex Sans and IBM Plex Serif fonts under the SIL Open Font License;
- refined Editorial, Ocean, Grayscale, and accessible Okabe-Ito categorical palettes;
- sequential and diverging continuous color maps;
- common journal and manuscript width profiles;
- practical recipes for interval, forest, distribution, trend, association, and small-multiple plots;
- a detailed visual and statistical review checklist;
- automated PDF/SVG/PNG export and palette-separation audits;
- caption and alt-text conventions.

The bundled IBM Plex fonts are distributed under the SIL Open Font License 1.1; see `assets/fonts/OFL.txt`.

## Install

Clone the repository into your Codex skills directory:

```bash
git clone https://github.com/ziruiKong/publication-chart-designer.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/publication-chart-designer"
```

Then invoke:

```text
Use $publication-chart-designer to create a publication-ready chart from this dataset.
```

## Example

Copy `scripts/figure_kit.py` and the complete `assets/` directory into the analysis project:

```python
from figure_kit import publication_figure, save_publication_figure, use_publication_style

use_publication_style(
    "assets/publication.mplstyle",
    palette="editorial",
    typography="sans",
)
fig, ax = publication_figure(width="single", ratio=0.64)
# Plot the audited data here.
save_publication_figure(fig, "figures/figure_02_policy_effects")
```

Audit the exported files:

```bash
python scripts/audit_figure.py figures/figure_02_policy_effects.pdf \
  figures/figure_02_policy_effects.png
python scripts/palette_audit.py --palette all
```
