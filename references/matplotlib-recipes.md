# Matplotlib Recipes

Use these patterns as starting points. Preserve the statistical choices and final physical dimensions requested by the user; do not copy every decoration into every figure.

## Shared Setup

```python
import matplotlib.pyplot as plt
import numpy as np
from figure_kit import (
    colormap,
    panel_label,
    publication_figure,
    reference_line,
    save_publication_figure,
    set_palette,
    use_publication_style,
)

use_publication_style(
    "assets/publication.mplstyle",
    palette="editorial",
    typography="sans",
)
colors = set_palette("editorial")
fig, ax = publication_figure(width="single", ratio=0.64)
```

Use `colors[0]`, `colors[1]`, `colors[2]`, and the other values consistently across panels. Reserve gray for context and secondary information.

## Dot and Interval Plot

Use for a small set of estimates, rates, or group means with uncertainty.

```python
labels = ["Control", "Local campaign", "National campaign"]
estimate = np.array([0.41, 0.48, 0.53])
low = np.array([0.36, 0.43, 0.48])
high = np.array([0.46, 0.53, 0.58])
y = np.arange(len(labels))

ax.errorbar(
    estimate,
    y,
    xerr=np.vstack([estimate - low, high - estimate]),
    fmt="o",
    color=colors[0],
    ecolor=colors[0],
    elinewidth=1.2,
    capsize=2.5,
    markersize=4.5,
)
ax.set_yticks(y, labels)
ax.set_xlabel("Probability of turnout (percentage points)")
ax.grid(axis="x")
```

Explain the interval in the caption. Avoid a bar chart when the comparison is mainly among estimates or when the baseline is not meaningful.

## Coefficient or Forest Plot

Use for models with several coefficients on a shared scale.

```python
order = np.argsort(estimate)
labels = np.asarray(labels)[order]
estimate, low, high = estimate[order], low[order], high[order]
y = np.arange(len(labels))

reference_line(ax, 0, axis="x", label="No association")
ax.hlines(y, low, high, color="#B8C0CC", linewidth=1.2)
ax.plot(estimate, y, "o", color=colors[0], markersize=4.5)
ax.set_yticks(y, labels)
ax.set_xlabel("Difference in outcome (95% CI)")
```

Do not sort by statistical significance. Sort by substantively interpretable order or effect size and state the choice.

## Distribution With Raw Observations

Use when central tendency could hide skew, clusters, or outliers.

```python
rng = np.random.default_rng(20261116)
groups = {
    "Control": rng.normal(0.00, 0.55, 80),
    "Treatment": rng.normal(0.35, 0.60, 80),
}

ax.boxplot(
    groups.values(),
    widths=0.32,
    showfliers=False,
    patch_artist=True,
    boxprops={"facecolor": "#F3F6FA", "edgecolor": "#64748B"},
    medianprops={"color": colors[0], "linewidth": 1.4},
    whiskerprops={"color": "#64748B"},
    capprops={"color": "#64748B"},
)
for position, values in enumerate(groups.values(), start=1):
    jitter = rng.uniform(-0.08, 0.08, size=len(values))
    ax.scatter(
        position + jitter,
        values,
        s=9,
        alpha=0.45,
        color=colors[0] if position == 1 else colors[1],
        edgecolors="none",
    )
ax.set_xticks([1, 2], groups.keys())
ax.set_ylabel("Outcome (units)")
```

Use deterministic jitter. State whether whiskers represent 1.5×IQR or another rule, or replace them with the interval meaningful to the design.

## Time Trend With Direct Labels

Use for a few series over time.

```python
series = {
    "Group A": np.array([0.21, 0.24, 0.25, 0.29, 0.31]),
    "Group B": np.array([0.19, 0.20, 0.23, 0.24, 0.27]),
}
series_colors = [colors[0], colors[1]]

for (label, values), color in zip(series.items(), series_colors):
    ax.plot(years, values, marker="o", color=color, label=label)
    ax.annotate(
        label,
        (years[-1], values[-1]),
        xytext=(5, 0),
        textcoords="offset points",
        va="center",
        color=color,
    )

ax.set_xlabel("Year")
ax.set_ylabel("Share (proportion)")
ax.grid(axis="y")
ax.margins(x=0.12)
```

Keep raw points visible when only a handful of periods are shown. If a smoother is needed, disclose its method and show raw observations where feasible.

## Association Plot

Use for relationship between two continuous variables.

```python
ax.scatter(
    x,
    y,
    s=13,
    alpha=0.55,
    color=colors[0],
    edgecolors="none",
)

# Show a fitted line only when its method is stated and appropriate.
ax.plot(fit_x, fit_y, color=colors[1], linewidth=1.4)
ax.set_xlabel("Exposure (units)")
ax.set_ylabel("Outcome (units)")
```

Do not connect observations from ordered units, and do not use a fitted line to imply causality from an observational association.

## Small Multiples

Use when panels share a scale and invite comparison.

```python
fig, axes = publication_figure(
    width="double",
    ratio=0.34,
    nrows=1,
    ncols=3,
    sharex=True,
    sharey=True,
)

for ax, (title, values) in zip(np.ravel(axes), panels.items()):
    ax.plot(years, values, color=colors[0], marker="o")
    ax.set_title(title, loc="left")

for label, ax in zip("ABC", np.ravel(axes)):
    panel_label(ax, label)
```

Use one y-axis range unless panel-specific ranges are scientifically necessary. If they differ, make the difference obvious and explain why.

## Reference Lines and Annotations

Add only annotations that help decode the data:

```python
reference_line(ax, 0, axis="y", label="No change")
ax.annotate(
    "Policy introduced",
    xy=(policy_date, event_value),
    xytext=(8, 10),
    textcoords="offset points",
    arrowprops={"arrowstyle": "-", "color": "#64748B", "linewidth": 0.8},
)
```

Place labels so they remain inside the exported canvas. Avoid arrows that point to positions not present in the source data.

## Continuous Color

Use a perceptually ordered map for magnitude and a diverging map only around a meaningful midpoint:

```python
mesh = ax.imshow(
    values,
    origin="lower",
    aspect="auto",
    cmap=colormap("sequential"),
)
fig.colorbar(mesh, ax=ax, label="Exposure (units)")
```

State what the color encodes and avoid rainbow or jet maps.

## Export

```python
paths = save_publication_figure(
    fig,
    "figures/figure_03_treatment_effects",
    formats=("pdf", "svg", "png"),
    dpi=600,
)
print("\n".join(str(path) for path in paths))
```

Open at least the final-size PNG after export. The script completing without error is not evidence that the figure is legible.
