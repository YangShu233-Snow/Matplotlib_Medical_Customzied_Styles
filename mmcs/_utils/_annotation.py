from __future__ import annotations

from typing import List, Optional

import numpy as np
from matplotlib.axes import Axes


def draw_sample_sizes(
    ax: Axes,
    data: List[np.ndarray],
    x_positions: np.ndarray,
    offset: Optional[float] = None,
    offset_factor: Optional[float] = None,
    fontsize: float = 10,
) -> None:
    for i, d in enumerate(data):
        n = len(d)
        top_val = np.max(d)

        if offset is not None:
            y_pos = top_val + offset
        elif offset_factor is not None:
            y_pos = top_val + float(np.std(d)) * offset_factor
        else:
            y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
            y_pos = top_val + y_range * 0.02

        ax.text(
            x_positions[i],
            y_pos,
            f"n={n}",
            ha="center",
            va="bottom",
            fontsize=fontsize,
        )
