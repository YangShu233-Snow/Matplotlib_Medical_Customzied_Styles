from pathlib import Path

import numpy as np

from mmcs import box_chart, save_figure

root = Path(__file__).parent

np.random.seed(12)
data = [
    np.random.normal(500, 150, 40),
    np.random.normal(900, 100, 40),
    np.random.normal(380, 80, 40),
]

result = box_chart(
    data=data,
    groups=["Sample A", "Sample B", "Sample C"],
    ylabel="Value",
    title="Boxplot",
)

save_figure(result.fig, root / "img", "boxplot_graphpad")
