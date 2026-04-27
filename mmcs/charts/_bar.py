from __future__ import annotations

from typing import Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes


def render(
    ax: Axes,
    data: Sequence[float],
    *,
    groups: Optional[Sequence[str]] = None,
    errors: Optional[Sequence[float]] = None,
    upper_only: bool = True,
    colors: Optional[Sequence[str]] = None,
    width: float = 0.6,
    stars: Optional[Sequence[int]] = None,
    edge: bool = True,
) -> Axes:
    x_pos = np.arange(len(data))
    means = np.asarray(data)

    yerr = None
    if errors is not None:
        if upper_only:
            yerr = [[0] * len(data), list(errors)]
        else:
            yerr = list(errors)

    edgecolor = plt.rcParams.get("patch.edgecolor") if edge else None
    ax.bar(x_pos, means, yerr=yerr, width=width, color=colors, edgecolor=edgecolor)

    if stars is not None:
        _draw_stars_simple(ax, means, errors or [0] * len(data), stars)

    if groups is not None:
        ax.set_xticks(x_pos)
        ax.set_xticklabels(list(groups))

    ax.set_xlim(-0.6, len(data) - 1 + 0.6)
    return ax


def _draw_stars_simple(
    ax: Axes,
    means: np.ndarray,
    errs: Sequence[float],
    stars: Sequence[int],
) -> None:
    for idx, n_stars in enumerate(stars):
        y_pos = means[idx] + errs[idx] + errs[idx] * 0.05
        ax.text(idx, y_pos, "*" * n_stars, ha="center", va="bottom")
