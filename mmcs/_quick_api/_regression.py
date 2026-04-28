from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Union

import matplotlib.pyplot as plt
import numpy as np

from mmcs._context import StyleContext
from mmcs._quick_api import ChartResult, _handle_save
from mmcs._registry import Style
from mmcs.charts import regression


def regression_chart(
    x: Any,
    y: Any,
    *,
    style: Union[str, Style] = "graphpad_prism",
    save_as: Optional[Union[str, Path]] = None,
    figsize: Optional[tuple[float, float]] = None,
    dpi: int = 300,
    xlabel: str = "X Value",
    ylabel: str = "Y Value",
    title: Optional[str] = None,
) -> ChartResult:
    ctxt = StyleContext(style)
    ctxt.apply(plt.rcParams, "regression")
    if figsize is None:
        figsize = (5, 5)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    regression.render(ax, x, y, xlabel=xlabel, ylabel=ylabel)

    if title:
        ax.set_title(title)

    _handle_save(fig, save_as)
    return ChartResult(fig, stats={"n_points": len(np.asarray(x))})
