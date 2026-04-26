from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

root_path = Path(__file__).parent
style_file = root_path / './assets/single_bubbleplot_chart.mplstyle'
plt.style.use(style_file)

def calculate_x_lim(
        x_values: np.ndarray
    )->Tuple[int, int]:

    x_max, x_min = x_values.max(), x_values.min()

    if x_min < 100:
        x_min_lim = x_min - x_min % 10
    else:
        x_min_lim = x_min - x_min % 100

    if x_max < 100:
        x_max_lim = (x_max // 10 + 2) * 10
    else:
        x_max_lim = (x_max // 100 + 2) * 100

    return x_min_lim, x_max_lim

def sort_by_color(
        color_data: np.ndarray,
        categories: List[str],
        x_values: np.ndarray,
        bubble_size_data: np.ndarray,
    ) -> Tuple[np.ndarray, List[str], np.ndarray, np.ndarray]:

    sorted_index = np.argsort(color_data)[::-1]
    return (
        color_data[sorted_index],
        [categories[i] for i in sorted_index],
        x_values[sorted_index],
        bubble_size_data[sorted_index]
    )


def main():
    # --- config ---
    img_name = 'example'
    title = 'Title'
    legend_label = 'legend'
    x_label  = 'Value'

    color_highlight = True
    p_value_ticks = True    # True: 标准 P 值阈值; False: 均匀等分


    # 模拟数据
    np.random.seed(12)
    categories = [f'Sample_{chr(index)}' for index in range(ord('A'), ord('N'))]
    x_values = np.random.normal(20, 10, len(categories))

    bubble_size_data = np.random.normal(50, 20, len(categories))
    color_data = np.random.randint(5, 100, len(categories)) / 1000

    min_bubble_size = 20
    max_bubble_size = 100

    percentile = [0, 0.50, 1]

    # --- ---

    if color_highlight:
        color_data, categories, x_values, bubble_size_data = sort_by_color(
            color_data, categories, x_values, bubble_size_data
        )

    y_index = np.arange(len(categories))

    size_scaled: np.ndarray[np.float64] = (
        (bubble_size_data - bubble_size_data.min()) /
        (bubble_size_data.max() - bubble_size_data.min()) *
        (max_bubble_size - min_bubble_size) +
        min_bubble_size
    )

    # --- figure: 2x2 GridSpec ---
    fig = plt.figure(figsize=(8, 8))
    gs = GridSpec(2, 2, width_ratios=[4, 1], hspace=0, wspace=0.02)

    ax = fig.add_subplot(gs[:, 0])          # scatter: left column, both rows
    ax_legend = fig.add_subplot(gs[0, 1])   # legend: top right
    ax_cbar = fig.add_subplot(gs[1, 1])     # colorbar: bottom right

    # 从 prop_cycle 读取颜色构建全色谱
    if color_highlight:
        prop_cycle = plt.rcParams['axes.prop_cycle']
        cmap_colors = [c['color'] for c in prop_cycle]
        cmap = LinearSegmentedColormap.from_list('', cmap_colors)
    else:
        cmap = LinearSegmentedColormap.from_list('', ['#999999', '#999999'])

    scatter = ax.scatter(
        x=x_values,
        y=y_index,
        s=size_scaled,
        c=color_data,
        cmap=cmap
    )

    ax.set_yticks(y_index)
    ax.set_yticklabels(categories)
    ax.set_xlabel(x_label)
    ax.set_xlim(*calculate_x_lim(x_values))

    # 图例 (右上)
    legend_sizes = [int(np.percentile(x_values, percent * 100)) for percent in percentile]

    legend_handles = []
    for val in legend_sizes:
        val_scaled = (val - bubble_size_data.min()) / (bubble_size_data.max() - bubble_size_data.min()) * \
                    (max_bubble_size - min_bubble_size) + min_bubble_size

        handle = ax.scatter([], [], s=val_scaled, c='#999999')
        legend_handles.append(handle)

    ax_legend.axis('off')
    leg = ax_legend.legend(
        handles=legend_handles,
        labels=[str(val) for val in legend_sizes],
        title=legend_label,
        loc='center',
        frameon=False
    )
    leg.get_title().set_ha('center')

    if color_highlight:
        # Colorbar (右下)
        ax_cbar.axis('off')
        cax = inset_axes(ax_cbar, width="15%", height="40%", loc='center')
        cax.set_frame_on(False)
        cbar = fig.colorbar(scatter, cax=cax, orientation="vertical")

        cax.set_title('P_value', pad=12, loc='center', fontsize=11)
        cax.tick_params(length=0)

        if p_value_ticks:
            standard_thresholds = [0.0001, 0.0005] + [0.001, 0.005] + [0.02 * n for n in range(1, 5, 1)] + [0.1, 0.5]
            ticks = [t for t in standard_thresholds if color_data.min() <= t <= color_data.max()]
        else:
            ticks = np.linspace(color_data.min(), color_data.max(), 4)

        cbar.set_ticks(ticks)
        cbar.set_ticklabels([f'{t:.3f}' for t in ticks])
    else:
        ax_cbar.axis('off')

    ax.set_title(title)

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

    plt.close('all')


if __name__ == '__main__':
    main()
