from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Sequence, Union

import matplotlib.pyplot as plt

from mmcs._context import StyleContext
from mmcs._quick_api import ChartResult, _handle_save, _label, _resolve_frame
from mmcs._registry import Style
from mmcs.charts import bar


def bar_chart(
    data: Any,
    groups: Optional[Sequence[str]] = None,
    errors: Optional[Sequence[float]] = None,
    *,
    x: Optional[str] = None,
    y: Optional[str] = None,
    style: Union[str, Style] = "graphpad_prism",
    save_as: Optional[Union[str, Path]] = None,
    figsize: Optional[tuple[float, float]] = None,
    dpi: int = 300,
    upper_only: bool = True,
    colors: Optional[Sequence[str]] = None,
    stars: Optional[Sequence[int]] = None,
    width: float = 0.6,
    edge: bool = True,
    title: Optional[str] = None,
    ylabel: Optional[str] = None,
    **kwargs: Any,
) -> ChartResult:
    arr, grp = _resolve_frame(data, x, y)
    ctxt = StyleContext(style)
    ctxt.apply(plt.rcParams, "bar")
    if figsize is None:
        figsize = (len(arr) * 1.5, 4)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    if colors is None:
        colors = ctxt.bar_colors(len(arr))
    bar.render(ax, arr, groups=grp if grp is not None else groups,
               errors=errors, colors=colors, stars=stars, width=width,
               upper_only=upper_only, edge=edge, **kwargs)
    _label(ax, ylabel=ylabel, title=title)
    _handle_save(fig, save_as)
    return ChartResult(fig, stats={"n_groups": len(arr)})
