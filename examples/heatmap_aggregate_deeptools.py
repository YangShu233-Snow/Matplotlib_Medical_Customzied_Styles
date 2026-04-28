from pathlib import Path

import numpy as np

from mmcs import heatmap_aggregate_chart, save_figure

root = Path(__file__).parent

np.random.seed(12)
rows, cols = 2000, 100

x = np.linspace(-3, 3, cols)
peak = np.exp(-(x**2) / 0.5) * 3
row_multipliers = np.linspace(1.5, 0.2, rows)[:, np.newaxis]

data_treat = peak * row_multipliers + np.random.normal(0, 0.5, (rows, cols))
data_ctrl = np.random.normal(-1.5, 1.5, (rows, cols))

treat = np.clip(data_treat, -3.5, 3)
ctrl = np.clip(data_ctrl, -3.5, 3)

result = heatmap_aggregate_chart(
    data=[treat, ctrl],
    titles=["Treatment", "Control"],
    style="deeptools",
    vmin=-3.5,
    vmax=3.0,
    colorbar_label="$\\log_2$FC CLIP/input",
    scale=0.5,
    scale_label="1 kb",
    ylabel="Enriched windows",
    title="Aggregate Genomic Heatmap",
)

save_figure(result.fig, root / "img", "heatmap_aggregate_deeptools", tight_layout=False)
