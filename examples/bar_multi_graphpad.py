from pathlib import Path

import matplotlib.pyplot as plt

from mmcs import StyleContext, save_figure
from mmcs.charts import bar

root = Path(__file__).parent
ctxt = StyleContext("graphpad_prism")

datasets = [
    (["Con", "KO"], [1200, 3500], [300, 400], [0, 3]),
    (["WT", "Mut"], [800, 2200], [200, 300], [0, 4]),
]

ctxt.apply(plt.rcParams, chart_type="bar")
fig, axs = plt.subplots(1, len(datasets), figsize=(8, 4))
plt.subplots_adjust(wspace=0.8)

for ax, (groups, means, errs, stars) in zip(axs, datasets):
    bar.render(ax, means, groups=groups, errors=errs, stars=stars,
               colors=ctxt.bar_colors(len(means)))
    ax.set_ylabel("Value")
    ax.set_title(f"{groups[0]} vs {groups[1]}")

save_figure(fig, root / "img", "bar_multi_graphpad")
