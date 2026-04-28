from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np

from mmcs._context import StyleContext
from mmcs._quick_api import ChartResult, _handle_save, _label
from mmcs._registry import Style
from mmcs.charts import boxviolin


def box_violin_chart(
    data: Any,
    groups: Optional[Sequence[str]] = None,
    *,
    style: Union[str, Style] = "graphpad_prism",
    save_as: Optional[Union[str, Path]] = None,
    figsize: Optional[tuple[float, float]] = None,
    dpi: int = 300,
    split: bool = False,
    split_labels: Optional[list[str]] = None,
    bandwidth: str = "scott",
    v_widths: float = 0.7,
    b_widths: float = 0.1,
    points: int = 60,
    cut: float = 1.5,
    show_n: bool = True,
    title: Optional[str] = None,
    ylabel: Optional[str] = None,
) -> ChartResult:
    ctxt = StyleContext(style)
    ctxt.apply(plt.rcParams, "box_violin")
    if figsize is None:
        figsize = (5, 5)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    if split:
        handles = boxviolin.render_split(
            ax, data, v_widths=v_widths, b_widths=b_widths,
            points=points, cut=cut, bandwidth=bandwidth,
            labels=split_labels, show_n=show_n,
        )
        if split_labels:
            ax.legend(handles=handles, frameon=False, loc="upper right")
    else:
        boxviolin.render(
            ax, data, v_widths=v_widths, b_widths=b_widths,
            points=points, cut=cut, bandwidth=bandwidth,
            show_n=show_n,
        )

    x_positions = np.arange(len(data))
    ax.set_xticks(x_positions)
    if groups is not None:
        ax.set_xticklabels(list(groups))

    _label(ax, ylabel=ylabel, title=title)
    _handle_save(fig, save_as)
    return ChartResult(fig, stats={"n_groups": len(data)})
