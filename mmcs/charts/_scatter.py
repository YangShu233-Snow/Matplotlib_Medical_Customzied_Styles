from __future__ import annotations

from typing import Any, Optional, Sequence

import numpy as np
from matplotlib.axes import Axes


def render(
    ax: Axes,
    x: Sequence[float],
    y: Sequence[float],
    *,
    c: Any = None,
    s: float = 20.0,
    cmap: Optional[str] = None,
) -> Axes:
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    ax.scatter(x_arr, y_arr, c=c, cmap=cmap, s=s)

    return ax
