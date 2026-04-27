from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt


def save_figure(
    fig: plt.Figure,
    save_dir: Union[str, Path],
    img_name: str,
    formats: Optional[Sequence[str]] = None,
    dpi: int = 300,
    bbox_inches: str = "tight",
    tight_layout: bool = True,
) -> list[Path]:
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    if formats is None:
        formats = ("png", "pdf")

    if tight_layout:
        fig.tight_layout()

    saved: list[Path] = []
    for ext in formats:
        path = save_dir / f"{img_name}.{ext}"
        fig.savefig(path, dpi=dpi, bbox_inches=bbox_inches)
        saved.append(path)

    return saved
