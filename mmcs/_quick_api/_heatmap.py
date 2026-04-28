from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np

from mmcs._context import StyleContext
from mmcs._quick_api import ChartResult, _handle_save_gs
from mmcs._registry import Style
from mmcs.charts import heatmap, heatmap_aggregate


def heatmap_chart(
    data: Any,
    *,
    row_labels: Optional[Sequence[str]] = None,
    col_labels: Optional[Sequence[str]] = None,
    style: Union[str, Style] = "deeptools",
    save_as: Optional[Union[str, Path]] = None,
    figsize: Optional[tuple[float, float]] = None,
    dpi: int = 300,
    vmin: float = -3.0,
    vmax: float = 3.0,
    cmap: Optional[str] = None,
    colorbar_label: str = "",
    title: Optional[str] = None,
) -> ChartResult:
    ctxt = StyleContext(style)
    ctxt.apply(plt.rcParams, "heatmap_clustered")
    if figsize is None:
        n_genes, n_samples = np.asarray(data).shape
        figsize = (max(5, n_samples * 0.3), max(5, n_genes * 0.15))
    fig = plt.figure(figsize=figsize, dpi=dpi)
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 5], height_ratios=[1, 5],
                          wspace=0.01, hspace=0.01)

    meta = heatmap.render(
        fig, gs, data,
        row_labels=row_labels, col_labels=col_labels,
        vmin=vmin, vmax=vmax, cmap=cmap,
        colorbar_label=colorbar_label,
    )

    if title:
        fig.suptitle(title, y=0.95)

    _handle_save_gs(fig, save_as)
    return ChartResult(fig, stats={"n_genes": meta["row_order"], "n_samples": meta["col_order"]})


def heatmap_aggregate_chart(
    data: Any,
    *,
    titles: Optional[Sequence[str]] = None,
    style: Union[str, Style] = "deeptools",
    save_as: Optional[Union[str, Path]] = None,
    figsize: Optional[tuple[float, float]] = None,
    dpi: int = 300,
    vmin: float = -3.5,
    vmax: float = 3.0,
    cmap: Optional[str] = None,
    colorbar_label: str = "",
    scale: float = 0.5,
    scale_label: str = "1 kb",
    ylabel: Optional[str] = None,
    title: Optional[str] = None,
) -> ChartResult:
    ctxt = StyleContext(style)
    ctxt.apply(plt.rcParams, "heatmap_multi")

    if isinstance(data, np.ndarray):
        data = [data]
        titles = titles or [""]

    n = len(data)
    if figsize is None:
        figsize = (n * 1.5 + 0.2, 6)
    fig, axs = plt.subplots(1, n, figsize=figsize, dpi=dpi, sharey=True)
    plt.subplots_adjust(wspace=0.1, bottom=0.25)
    if n == 1:
        axs = [axs]

    heatmap_aggregate.render(
        axs, data,
        titles=titles, vmin=vmin, vmax=vmax, cmap=cmap,
        colorbar_label=colorbar_label, scale=scale, scale_label=scale_label,
        ylabel=ylabel,
    )

    if title:
        fig.suptitle(title, y=0.95)

    _handle_save_gs(fig, save_as)
    return ChartResult(fig, stats={"n_panels": n})
