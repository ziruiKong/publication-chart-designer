"""Reusable Matplotlib helpers for polished publication figures.

Copy this file and the ``assets`` directory into the analysis project. The
helpers keep typography, color, physical dimensions, panel labels, reference
lines, and exports consistent without hiding the actual plotting decisions.
"""

from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap


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
    "nature-single": 3.50,
    "nature-double": 7.20,
    "science-single": 2.17,
    "science-double": 4.72,
    "science-triple": 7.20,
    "ieee-single": 3.50,
    "ieee-double": 7.16,
    "plos-full": 7.50,
    "apa-page": 6.50,
}

DEFAULT_PALETTE = "editorial"
_PALETTE_CACHE: dict[Path, dict] = {}
_ACTIVE_PALETTE_PATH: Path | None = None


def _asset_dir() -> Path:
    script_dir = Path(__file__).resolve().parent
    candidates = (
        script_dir / "assets",
        script_dir.parent / "assets",
        Path.cwd() / "assets",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return script_dir.parent / "assets"


def _palette_data(palette_path: str | Path | None = None) -> dict:
    global _ACTIVE_PALETTE_PATH
    if palette_path:
        path = Path(palette_path)
    elif _ACTIVE_PALETTE_PATH:
        path = _ACTIVE_PALETTE_PATH
    else:
        path = _asset_dir() / "palettes.json"
    path = path.expanduser().resolve()

    if path not in _PALETTE_CACHE:
        if not path.exists():
            raise FileNotFoundError(f"Palette definitions not found: {path}")
        _PALETTE_CACHE[path] = json.loads(path.read_text(encoding="utf-8"))
    return _PALETTE_CACHE[path]


def register_bundled_fonts(font_dir: str | Path | None = None) -> list[Path]:
    """Register the bundled IBM Plex font files with Matplotlib."""

    directory = Path(font_dir) if font_dir else _asset_dir() / "fonts"
    directory = directory.expanduser().resolve()
    if not directory.exists():
        warnings.warn(
            f"Bundled fonts not found at {directory}; Matplotlib will use fallback fonts",
            RuntimeWarning,
            stacklevel=2,
        )
        return []

    fonts = sorted(directory.glob("*.ttf"))
    for font in fonts:
        font_manager.fontManager.addfont(str(font))
    return fonts


def set_font_family(
    families: Sequence[str],
    base_size: float | None = None,
) -> None:
    """Set an ordered font-family fallback list and optional base size."""

    if not families:
        raise ValueError("at least one font family is required")
    mpl.rcParams["font.family"] = list(families)
    if base_size is not None:
        if base_size <= 0:
            raise ValueError("base_size must be positive")
        mpl.rcParams["font.size"] = float(base_size)
        mpl.rcParams["axes.titlesize"] = float(base_size) + 1
        mpl.rcParams["figure.titlesize"] = float(base_size) + 3
        mpl.rcParams["axes.labelsize"] = float(base_size)
        mpl.rcParams["xtick.labelsize"] = max(float(base_size) - 1, 5)
        mpl.rcParams["ytick.labelsize"] = max(float(base_size) - 1, 5)
        mpl.rcParams["legend.fontsize"] = max(float(base_size) - 1, 5)


def set_typography(profile: str = "sans", base_size: float | None = None) -> None:
    """Apply a modern sans or scholarly serif typographic profile."""

    profiles = {
        "sans": ["IBM Plex Sans", "DejaVu Sans"],
        "serif": ["IBM Plex Serif", "DejaVu Serif"],
    }
    key = profile.lower()
    if key not in profiles:
        raise ValueError(f"Unknown typography profile: {profile}")

    set_font_family(profiles[key], base_size)
    if key == "sans":
        mpl.rcParams["mathtext.rm"] = "IBM Plex Sans"
        mpl.rcParams["mathtext.it"] = "IBM Plex Sans:italic"
        mpl.rcParams["mathtext.bf"] = "IBM Plex Sans:semibold"
    else:
        mpl.rcParams["mathtext.rm"] = "IBM Plex Serif"
        mpl.rcParams["mathtext.it"] = "IBM Plex Serif:italic"
        mpl.rcParams["mathtext.bf"] = "IBM Plex Serif:semibold"


def available_palettes(palette_path: str | Path | None = None) -> dict[str, str]:
    """Return palette keys and user-facing labels."""

    data = _palette_data(palette_path)
    return {key: value["label"] for key, value in data["palettes"].items()}


def palette_colors(
    name: str = DEFAULT_PALETTE,
    palette_path: str | Path | None = None,
) -> tuple[str, ...]:
    """Return a named categorical palette."""

    data = _palette_data(palette_path)
    palettes = data["palettes"]
    if name not in palettes:
        choices = ", ".join(sorted(palettes))
        raise ValueError(f"Unknown palette '{name}'. Available: {choices}")
    return tuple(palettes[name]["colors"])


def set_palette(
    name: str = DEFAULT_PALETTE,
    palette_path: str | Path | None = None,
) -> tuple[str, ...]:
    """Set the Matplotlib color cycle to a named categorical palette."""

    colors = palette_colors(name, palette_path)
    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=colors)
    return colors


def colormap(
    name: str = "sequential",
    palette_path: str | Path | None = None,
) -> LinearSegmentedColormap:
    """Build a perceptually ordered custom continuous color map."""

    data = _palette_data(palette_path)
    maps = data["colormaps"]
    if name not in maps:
        choices = ", ".join(sorted(maps))
        raise ValueError(f"Unknown colormap '{name}'. Available: {choices}")
    return LinearSegmentedColormap.from_list(name, maps[name]["colors"])


def use_publication_style(
    style_path: str | Path | None = None,
    palette: str = DEFAULT_PALETTE,
    typography: str = "sans",
    font_dir: str | Path | None = None,
    context: str = "paper",
    language: str = "en",
) -> None:
    """Load the publication style, bundled fonts, palette, and typography."""

    global _ACTIVE_PALETTE_PATH
    sizes = {"paper": 8, "screen": 11, "slide": 14, "poster": 18}
    if context not in sizes or language not in {"en", "zh"}:
        raise ValueError("context: paper/screen/slide/poster; language: en/zh")
    if style_path is None:
        style_path = _asset_dir() / "publication.mplstyle"

    style_path = Path(style_path).expanduser().resolve()
    if not style_path.exists():
        raise FileNotFoundError(f"Matplotlib style not found: {style_path}")

    if font_dir is None:
        font_dir = style_path.parent / "fonts"
    register_bundled_fonts(font_dir)

    plt.style.use(style_path)
    set_typography(typography, base_size=sizes[context])
    if language == "zh":
        installed = {font.name for font in font_manager.fontManager.ttflist}
        candidates = ["Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Source Han Sans SC", "SimHei"]
        cjk = next((name for name in candidates if name in installed), None)
        if cjk:
            set_font_family([cjk, *mpl.rcParams["font.family"]])
        else:
            warnings.warn("No Chinese font detected; install Noto Sans CJK SC before rendering Chinese labels", RuntimeWarning, stacklevel=2)
    _ACTIVE_PALETTE_PATH = style_path.parent / "palettes.json"
    set_palette(palette, _ACTIVE_PALETTE_PATH)

    mpl.rcParams["figure.dpi"] = 120
    mpl.rcParams["savefig.transparent"] = False
    mpl.rcParams["svg.hashsalt"] = "publication-chart-designer"


def publication_figure(
    width: str | float = "single",
    ratio: float = 0.62,
    **kwargs,
):
    """Create a figure sized in inches at its intended output width."""

    if ratio <= 0:
        raise ValueError("ratio must be positive")

    if "figsize" not in kwargs:
        if isinstance(width, str):
            if width not in FIGURE_WIDTHS:
                choices = ", ".join(FIGURE_WIDTHS)
                raise ValueError(f"Unknown width profile '{width}'. Available: {choices}")
            inches = FIGURE_WIDTHS[width]
        else:
            inches = width
        kwargs["figsize"] = (float(inches), float(inches) * ratio)

    kwargs.setdefault("layout", "constrained")
    return plt.subplots(**kwargs)


def refine_axes(ax, grid: str | None = "y", max_ticks: int = 5):
    """Apply flat geometry to a numeric plot without changing its data limits.

    Skip tick locators for dates, log scales, and categorical axes; configure
    those locators explicitly. Call after plotting to detect unit converters.
    """
    from matplotlib.ticker import MaxNLocator

    if grid not in {None, "x", "y", "both"} or max_ticks < 2:
        raise ValueError("grid: None/x/y/both; max_ticks must be at least 2")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(False, which="both")
    if grid:
        ax.grid(True, axis=grid, which="major")
    ax.tick_params(which="major", pad=4)
    for axis in (ax.xaxis, ax.yaxis):
        if axis.get_scale() == "linear" and axis.get_converter() is None:
            from matplotlib.ticker import FixedLocator
            if not isinstance(axis.get_major_locator(), FixedLocator):
                axis.set_major_locator(MaxNLocator(nbins=max_ticks - 1))
    return ax


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
        "fontweight": "semibold",
        "fontsize": mpl.rcParams["font.size"] + 1,
        "color": mpl.rcParams["text.color"],
    }
    options.update(kwargs)
    return ax.text(x, y, label, transform=ax.transAxes, clip_on=False, **options)


def role_text(ax, x: float, y: float, text: str, role: str = "annotation", **kwargs):
    """Place axes-fraction prose with explicit weight and upright style.

    Put scientific italic in mathtext, e.g. r'$p$ = 0.03', rather than making
    a complete annotation italic. Venue conventions override the defaults.
    """
    base = float(mpl.rcParams["font.size"])
    roles = {
        "title": (base + 2, "semibold", "#172B3A"),
        "panel": (base + 1, "semibold", "#172B3A"),
        "body": (base, "normal", "#263746"),
        "annotation": (base - 1, "normal", "#465966"),
        "note": (base - 1, "normal", "#64748B"),
    }
    if role not in roles:
        raise ValueError(f"Unknown text role: {role}")
    size, weight, color = roles[role]
    options = dict(transform=ax.transAxes, fontsize=size, fontweight=weight,
                   fontstyle="normal", color=color, ha="left", va="top")
    options.update(kwargs)
    return ax.text(x, y, text, **options)


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
    crop: bool = False,
) -> list[Path]:
    """Save at the declared physical size; opt into tight cropping explicitly."""

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
            "bbox_inches": "tight" if crop else None,
            "pad_inches": pad_inches,
            "transparent": transparent,
        }
        if fmt in {"png", "jpg", "jpeg", "tif", "tiff"}:
            options["dpi"] = dpi
        if metadata and fmt in {"pdf", "svg", "png"}:
            options["metadata"] = metadata

        with mpl.rc_context({"savefig.bbox": "standard"}):
            fig.savefig(path, **options)
        if fmt == "svg":
            # Matplotlib emits trailing spaces inside path definitions. Keep
            # generated SVGs clean in version control without changing geometry.
            svg = path.read_text(encoding="utf-8")
            path.write_text("\n".join(line.rstrip() for line in svg.splitlines()) + "\n",
                            encoding="utf-8", newline="\n")
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
