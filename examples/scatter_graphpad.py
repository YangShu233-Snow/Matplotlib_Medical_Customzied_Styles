from pathlib import Path

import numpy as np

from mmcs import save_figure, scatter_chart

root = Path(__file__).parent

np.random.seed(12)
x = np.concatenate([np.random.normal(50, 10, 50), np.random.normal(500, 100, 50)])
y = np.concatenate([np.random.normal(600, 200, 50), np.random.normal(60, 10, 50)])

result = scatter_chart(
    x=x,
    y=y,
    xlabel="X Value",
    ylabel="Y Value",
    title="Scatter Chart",
)

save_figure(result.fig, root / "img", "scatter_graphpad")
