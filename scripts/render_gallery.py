"""Reproduce the README gallery using synthetic design data, not study results."""
from pathlib import Path
import argparse
import matplotlib
matplotlib.use("Agg")
import numpy as np
from matplotlib.ticker import PercentFormatter
from figure_kit import (
    use_publication_style, publication_figure, palette_colors, refine_axes,
    save_publication_figure, colormap,
)


def render(output):
    use_publication_style(context="screen")
    navy, accent = palette_colors()[:2]
    fig, axes = publication_figure(width=11.6, ratio=0.66, nrows=2, ncols=2)
    fig.get_layout_engine().set(w_pad=0.18, h_pad=0.18, wspace=0.12, hspace=0.14)
    fig.suptitle("Clear comparisons. Orderly geometry.", x=0.03, ha="left", fontsize=20, fontweight="semibold")
    fig.supxlabel("DESIGN GALLERY  /  Synthetic data for layout demonstration only", fontsize=9, color="#64748B")

    ax = axes[0, 0]
    x = np.arange(1, 7)
    for label, y, color, marker in [
        ("Group A", np.array([32, 39, 43, 52, 57, 64]), navy, "o"),
        ("Group B", np.array([28, 31, 36, 40, 43, 47]), accent, "s"),
    ]:
        ax.plot(x, y, color=color, marker=marker, label=label)
    ax.set(title="A   Trends", xlabel="Month", ylabel="Response (%)", ylim=(20, 70))
    ax.set_xticks(x)
    ax.legend(loc="upper left", ncols=2)
    refine_axes(ax)

    ax = axes[0, 1]
    ax.bar(["North", "East", "South", "West"], [42, 56, 63, 48], width=0.58,
           color=navy, edgecolor="none")
    ax.set(title="B   Categories", ylabel="Response (%)", ylim=(0, 80))
    refine_axes(ax)

    ax = axes[1, 0]
    means = np.array([0.15, 0.25, 0.32, 0.41])
    y = np.arange(4)
    ax.errorbar(means, y, xerr=[0.08, 0.06, 0.09, 0.07], fmt="o", color=navy,
                elinewidth=1.3, capsize=3, markersize=5)
    ax.set_yticks(y, ["Program A", "Program B", "Program C", "Program D"])
    ax.set(title="C   Estimates and intervals", xlabel="Difference (percentage points)",
           xlim=(0, 0.55), ylim=(-0.6, 3.6))
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.invert_yaxis()
    refine_axes(ax, grid="x")

    ax = axes[1, 1]
    matrix = np.array([[0.2, 0.3, 0.4, 0.5], [0.3, 0.5, 0.6, 0.7],
                       [0.4, 0.6, 0.7, 0.9]])
    mesh = ax.imshow(matrix, cmap=colormap(), vmin=0, vmax=1, aspect="equal")
    ax.set_anchor("W")
    ax.set(title="D   Ordered magnitude", xlabel="Stage", ylabel="Cohort")
    ax.set_xticks(range(4), ["I", "II", "III", "IV"])
    ax.set_yticks(range(3), ["A", "B", "C"])
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.colorbar(mesh, ax=ax, shrink=0.85, label="Score", ticks=[0, 0.5, 1])
    return save_publication_figure(fig, Path(output) / "flat-gallery", dpi=300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="docs/gallery")
    args = parser.parse_args()
    for path in render(args.output):
        print(path)
