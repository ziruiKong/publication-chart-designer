"""Reusable Matplotlib helpers for publication figures.

Copy this file and ``assets/publication.mplstyle`` into the analysis project.
The helpers keep final physical dimensions, panel labels, reference lines, and
exports consistent without hiding the actual plotting decisions.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt


COLORS = {
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "green": "#009E73",
    "purple": "#CC79A7",
    "orange": "#E69F00",
    "sky": "#56B4E9",
    "yellow": "#F0E442",
    "ink": "#111111",
    "gray": "#64748B",
}

PALETTE: tuple[str, ...] = (
    COLORS["blue"],
    COLORS["vermillion"],
    COLORS["green"],
    COLORS["purple"],
    COLORS["orange"],
    COLORS["sky"],
)

FIGURE_WIDTHS = {
    "single": 3.4,
    "1.5": 4.8,
    "double": 7.0,
}


def use_publication_style(style_path: str | Path | None = None) -> None:
    """Load the bundled style and the accessible default color cycle."""

    if style_path is None:
        style_path = Path(__file__).resolve().parents[1] / "assets" / "publication.mplstyle"

    style_path = Path(style_path).expanduser().resolve()
    if not style_path.exists():
        raise FileNotFoundError(f"Matplotlib style not found: {style_path}")

    plt.style.use(style_path)
    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=PALETTE)
    mpl.rcParams["figure.dpi"] = 120
    mpl.rcParams["savefig.transparent"] = False


def publication_figure(
    width: str | float = "single",
    ratio: float = 0.62,
    **kwargs,
):
    """Create a figure sized in inches at its intended output width."""

    if ratio <= 0:
        raise ValueError("ratio must be positive")

    if "figsize" not in kwargs:
        inches = FIGURE_WIDTHS.get(width, width) if isinstance(width, str) else width
        kwargs["figsize"] = (float(inches), float(inches) * ratio)

    kwargs.setdefault("layout", "constrained")
    return plt.subplots(**kwargs)


def panel_label(
    ax,
    label: str,
    x: float = -0.08,
    y: float = 1.04,
    **kwargs,
):
    """Place a consistent panel label relative to an axes box."""

    options = {
        "ha": "left",
        "va": "bottom",
        "fontweight": "bold",
        "fontsize": 9,
        "color": mpl.rcParams["text.color"],
    }
    options.update(kwargs)
    return ax.text(x, y, label, transform=ax.transAxes, clip_on=False, **options)


def reference_line(
    ax,
    value: float,
    axis: str = "y",
    label: str | None = None,
    **kwargs,
):
    """Draw a subtle reference line, optionally with a direct label."""

    options = {
        "color": "#94A3B8",
        "linewidth": 0.8,
        "linestyle": (0, (3, 3)),
        "zorder": 0,
    }
    options.update(kwargs)

    if axis == "x":
        line = ax.axvline(value, **options)
        if label:
            ax.annotate(
                label,
                xy=(value, 1),
                xycoords=("data", "axes fraction"),
                xytext=(4, -4),
                textcoords="offset points",
                ha="left",
                va="top",
                fontsize=7,
                color=options["color"],
            )
    elif axis == "y":
        line = ax.axhline(value, **options)
        if label:
            ax.annotate(
                label,
                xy=(1, value),
                xycoords=("axes fraction", "data"),
                xytext=(-4, 4),
                textcoords="offset points",
                ha="right",
                va="bottom",
                fontsize=7,
                color=options["color"],
            )
    else:
        raise ValueError("axis must be 'x' or 'y'")

    return line


def save_publication_figure(
    fig,
    stem: str | Path,
    formats: Iterable[str] = ("pdf", "svg", "png"),
    dpi: int = 600,
    transparent: bool = False,
    pad_inches: float = 0.02,
    metadata: dict[str, str] | None = None,
    close: bool = True,
) -> list[Path]:
    """Save one figure to a stable stem in each requested format."""

    target = Path(stem).expanduser()
    if target.suffix:
        target = target.with_suffix("")
    target.parent.mkdir(parents=True, exist_ok=True)

    requested = tuple(dict.fromkeys(fmt.lower().lstrip(".") for fmt in formats))
    if not requested:
        raise ValueError("at least one output format is required")

    paths: list[Path] = []
    for fmt in requested:
        path = target.with_suffix(f".{fmt}")
        options = {
            "format": fmt,
            "bbox_inches": "tight",
            "pad_inches": pad_inches,
            "transparent": transparent,
        }
        if fmt in {"png", "jpg", "jpeg", "tif", "tiff"}:
            options["dpi"] = dpi
        if metadata and fmt in {"pdf", "svg", "png"}:
            options["metadata"] = metadata

        fig.savefig(path, **options)
        paths.append(path)

    if close:
        plt.close(fig)
    return paths


def sparse_ticks(values: Sequence[float], count: int = 6) -> list[float]:
    """Choose readable tick positions without changing plotted data."""

    if count < 2:
        raise ValueError("count must be at least 2")
    import numpy as np

    return list(np.linspace(float(min(values)), float(max(values)), count))
