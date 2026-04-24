from typing import Dict, List

from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/single_volinplot_chart.mplstyle'
plt.style.use(style_file)

def scott_MISE(
        data: List[np.ndarray]
    )->float:
    n_avg = np.mean(data)
    return float(n_avg ** (-1/5))

def draw_split_violinplot(
        ax: Axes, 
        data: List[np.ndarray], 
        points: int, 
        widths: float,
        labels: List[str] = ['Group 1', 'Group 2']
    ):

    x_pos = np.arange(len(data))
    bw_method = scott_MISE([np.concatenate(d) for d in data])

    high_group = [sub_data[0] for sub_data in data]
    low_group = [sub_data[1] for sub_data in data]

    # 从 rcParams 的 prop_cycle 中获取颜色
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = [c['color'] for c in prop_cycle]

    handles = []
    for i, (side, group) in enumerate(zip(( 'low', 'high'), (low_group, high_group))):
        color = colors[i % len(colors)]
        parts = ax.violinplot(
            group,
            x_pos,
            points=points,
            widths=widths,
            bw_method=bw_method,
            side=side,
            showextrema=False
        )
        for pc in parts['bodies']:
            pc.set_facecolor(color)
            pc.set_edgecolor('black')
            pc.set_linewidth(1.5)
            pc.set_alpha(1)
        
        # 为图例创建 Patch
        from matplotlib.patches import Patch
        handles.append(Patch(facecolor=color, edgecolor='black', label=labels[i]))
    
    return handles

def main():
    # --- config ---
    title = 'Treatment Comparison'
    ylabel = 'Relative Expression'
    img_name = 'example_split'

    points = 60
    widths = 0.7
    labels = ['Control', 'Treatment']

    np.random.seed(12)
    # split 模式数据格式: [ [group1, group2], [group1, group2], ... ]
    data = [
        [np.random.normal(200, 50, 100), np.random.normal(250, 60, 100)],
        [np.random.normal(800, 150, 100), np.random.normal(700, 180, 100)],
        [np.random.normal(400, 80, 100), np.random.normal(500, 90, 100)]
    ]

    # --- figure ---
    fig, ax = plt.subplots(
        figsize=(6, 5)
    )

    handles = draw_split_violinplot(
        ax, data, points, widths, labels=labels
    )
    ax.legend(handles=handles, frameon=False, loc='upper right')

    # 应用配置中的标签和标题
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xticks(np.arange(len(data)))
    ax.set_xticklabels([f'Sample {i+1}' for i in range(len(data))])

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
