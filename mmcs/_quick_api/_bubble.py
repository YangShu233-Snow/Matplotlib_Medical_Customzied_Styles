from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np

from mmcs._context import StyleContext
from mmcs._quick_api import ChartResult, _handle_save_gs
from mmcs._registry import Style
from mmcs.charts import bubble


def bubble_chart(
    categories: Sequence[str],
    x_values: Any,
    bubble_sizes: Any,
    color_values: Any,
    *,
    style: Union[str, Style] = "ggplot",
    save_as: Optional[Union[str, Path]] = None,
    figsize: Optional[tuple[float, float]] = None,
    dpi: int = 300,
    xlabel: str = "Value",
    color_highlight: bool = True,
    legend_label: str = "legend",
    p_value_ticks: bool = True,
    title: Optional[str] = None,
) -> ChartResult:
    ctxt = StyleContext(style)
    ctxt.apply(plt.rcParams, "bubble")
    if figsize is None:
        figsize = (8, 8)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    gs = fig.add_gridspec(2, 2, width_ratios=[4, 1], hspace=0, wspace=0.02)

    bubble.render(
        fig, gs, categories,
        x_values=np.asarray(x_values),
        bubble_sizes=np.asarray(bubble_sizes),
        color_values=np.asarray(color_values),
        xlabel=xlabel, color_highlight=color_highlight,
        legend_label=legend_label, p_value_ticks=p_value_ticks,
    )

    if title:
        fig.suptitle(title, y=0.95)

    _handle_save_gs(fig, save_as)
    return ChartResult(fig, stats={"n_categories": len(categories)})
