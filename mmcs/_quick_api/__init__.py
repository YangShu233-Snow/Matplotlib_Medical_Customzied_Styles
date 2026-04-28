from __future__ import annotations

import base64
import io
from pathlib import Path
from typing import Any, Optional, Union

import matplotlib.pyplot as plt


class ChartResult:
    def __init__(self, fig: plt.Figure, stats: Optional[dict[str, Any]] = None):
        self.fig = fig
        self.stats = stats or {}

    def to_base64(self, fmt: str = "png", dpi: int = 300) -> str:
        buf = io.BytesIO()
        self.fig.savefig(buf, format=fmt, dpi=dpi, bbox_inches="tight")
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")


def _handle_save(fig: plt.Figure, save_as: Optional[Union[str, Path]]) -> None:
    if save_as is not None:
        fig.savefig(Path(save_as), bbox_inches="tight")
    else:
        fig.tight_layout()


def _handle_save_gs(fig: plt.Figure, save_as: Optional[Union[str, Path]]) -> None:
    if save_as is not None:
        fig.savefig(Path(save_as), bbox_inches="tight")


def _label(
    ax: plt.Axes,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    title: Optional[str] = None,
) -> None:
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)


def _resolve_frame(
    data: Any,
    x_col: Optional[str] = None,
    y_col: Optional[str] = None,
) -> tuple[Any, Optional[Any]]:
    if x_col is None and y_col is None:
        return data, None
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required when using x=/y= parameters") from None
    if not isinstance(data, pd.DataFrame):
        raise TypeError("x=/y= parameters require a pandas DataFrame")

    values = data[y_col].values if y_col else data
    groups = data[x_col].values if x_col else None
    return values, groups


from mmcs._quick_api._bar import bar_chart  # noqa: E402
from mmcs._quick_api._box import box_chart  # noqa: E402
from mmcs._quick_api._boxviolin import box_violin_chart  # noqa: E402
from mmcs._quick_api._bubble import bubble_chart  # noqa: E402
from mmcs._quick_api._density import density_chart  # noqa: E402
from mmcs._quick_api._heatmap import (  # noqa: E402
    heatmap_aggregate_chart,
    heatmap_chart,
)
from mmcs._quick_api._histogram import histogram_chart  # noqa: E402
from mmcs._quick_api._regression import regression_chart  # noqa: E402
from mmcs._quick_api._scatter import (  # noqa: E402
    scatter_chart,
    scatter_clustered_chart,
)
from mmcs._quick_api._violin import violin_chart  # noqa: E402

__all__ = [
    "ChartResult",
    "bar_chart",
    "box_chart",
    "box_violin_chart",
    "bubble_chart",
    "density_chart",
    "heatmap_aggregate_chart",
    "heatmap_chart",
    "histogram_chart",
    "regression_chart",
    "scatter_chart",
    "scatter_clustered_chart",
    "violin_chart",
]
