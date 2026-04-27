from __future__ import annotations

from typing import Any, Union

from matplotlib import pyplot as plt

from mmcs._registry import Style


class StyleContext:
    def __init__(self, style: Union[str, Style]) -> None:
        if isinstance(style, str):
            style = Style(style)
        self._style = style

    @property
    def name(self) -> str:
        return self._style.name

    @property
    def info(self) -> dict[str, Any]:
        return self._style.info

    def apply(self, rcParams: dict | None = None, chart_type: str | None = None) -> None:
        self._style.apply(rcParams, chart_type=chart_type)

    def bar_colors(self, n: int) -> list[str]:
        palette = self._read_palette()
        if n >= len(palette):
            return [palette[i % len(palette)] for i in range(n)]
        return [_uniform_sample(palette, i, n) for i in range(n)]

    def scatter_colors(self) -> list[str]:
        return self._read_palette()

    def box_colors(self) -> str:
        palette = self._read_palette()
        return palette[0] if palette else "CCCCCC"

    def _read_palette(self) -> list[str]:
        cycle = plt.rcParams.get("axes.prop_cycle")
        if cycle is not None:
            return [entry["color"] for entry in cycle]
        return []


def _uniform_sample(palette: list[str], idx: int, total: int) -> str:
    n = len(palette)
    k = round(idx * (n - 1) / (total - 1)) if total > 1 else 0
    return palette[k]
