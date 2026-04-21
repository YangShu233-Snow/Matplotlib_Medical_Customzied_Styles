import enum

import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
from typing import List, Tuple
from matplotlib.axes import Axes

root_path = Path(__file__).parent
style_file = root_path / './assets/single_clustered_columns_scatter_chart.mplstyle'
plt.style.use(style_file)

def calculate_star_y_position(mean: float, sem: float, top_val: float):
    star_y_postion_1 = mean + sem + sem * 0.05
    star_y_postion_2 = top_val + 20

    return star_y_postion_1 if star_y_postion_1 > star_y_postion_2 else star_y_postion_2


def draw_stars(ax: Axes, index_list: List[int], x_positions: List[float], stars_list: List[int], raw_data: List[np.ndarray], means: List[float], errs: List[float]):
    for index, i in enumerate(index_list):
        x_pos = x_positions[i]
        mean = means[i]
        err = errs[i]
        stars = stars_list[index]

        # 必须考虑到散点图的最大值，防止星号与散点重叠
        group_max = np.max(raw_data)
        error_max = mean + err
        top_val = max(group_max, error_max)
        
        star_y_position = calculate_star_y_position(mean, err, top_val)

        ax.text(x_pos, star_y_position, '*' * stars,
                ha='center', va='bottom', fontsize=14)

def generate_prism_colors(num_groups):
    if num_groups == 1:
        return ['black']

    grays = np.linspace(0, 0.8, num_groups)
    return [str(g) for g in grays]


def generate_jittered_x(y: np.ndarray, r_x: float, r_y: float) -> np.ndarray:
    """
    生成独立的X轴和Y轴防重叠抖动。
    
    :param y: 原数据的 Y 坐标
    :param r_x: X 轴方向的排斥半径 (通常很小，例如 0.02~0.05)
    :param r_y: Y 轴方向的排斥半径 (根据数据量级决定，例如 50~100)
    """
    n = len(y)
    x = np.zeros(n)
    
    # 分别计算 X 和 Y 方向的安全直径
    D_x = 2 * r_x
    D_y = 2 * r_y 

    sorted_indices = np.argsort(y, kind='stable')
    placed_indices = []
    
    for idx in sorted_indices:
        y_i = y[idx]
        
        # 1. 找到可能发生重叠的已放置点
        conflicts = []
        for prev_idx in reversed(placed_indices):
            dy = y_i - y[prev_idx]
            if dy >= D_y:
                break
            conflicts.append(prev_idx)
            
        if not conflicts:
            x[idx] = 0.0
            placed_indices.append(idx)
            continue
            
        # 2. 计算禁区 (使用椭圆公式)
        intervals = []
        for c_idx in conflicts:
            dy = y_i - y[c_idx]
            
            # 归一化 Y 距离的平方
            y_ratio_sq = (dy / D_y)**2
            if y_ratio_sq >= 1.0:
                continue
                
            # 根据椭圆方程计算 X 轴需要偏移的最小距离
            dx = D_x * np.sqrt(1.0 - y_ratio_sq) + 1e-8
            
            x_c = x[c_idx]
            intervals.append((x_c - dx, x_c + dx))
            
        # 3. 收集候选点
        candidates = [0.0]
        for iv in intervals:
            candidates.extend([iv[0], iv[1]])
        candidates.sort(key=lambda val: (abs(val), val))
        
        # 4. 寻找最优位置
        chosen_x = 0.0
        for cand in candidates:
            is_valid = True
            for iv in intervals:
                if iv[0] < cand < iv[1]:
                    is_valid = False
                    break
            if is_valid:
                chosen_x = cand
                break
                
        x[idx] = chosen_x
        placed_indices.append(idx)
        
    return np.asarray(x, dtype=float)

def main():
    # --- 配置区 ---
    ylabel = 'Value'
    title = 'Title'
    img_name = 'example.png'

    # --- 示例数据 ---
    # 大类别（X轴的主刻度）
    categories = [
        ('Group A', ['CON', 'KO']), 
        ('Group B', ['CON', 'KO']), 
        ('Group C', ['CON', 'KO'])
        ]
    
    all_raw_data = [
        [np.random.normal(1200, 300, 15), np.random.normal(3500, 400, 15)],
        [np.random.normal(1500, 200, 20), np.random.normal(2200, 300, 20)],
        [np.random.normal(1100, 150, 15), np.random.normal(1050, 100, 15)]
    ]

    # 将数据组织为 2D 数组（或者列表的列表）：形状为 (子组数量, 类别数量)
    # 每一行代表一个子组(例如'Con')在所有类别上的值
    all_means = []
    all_errs = []
    for raw_data in all_raw_data:
        all_means.append([np.mean(data) for data in raw_data])
        all_errs.append([np.std(data, ddof=1) / np.sqrt(len(data)) for data in raw_data])
    
    # 显著性星号标记: (类别索引, 子组索引, 星号数量)
    # 例如：(0, 1, 3) 代表给第0个类别(Gene A)的第1个子组(KO)打上3个星号(***)
    stars_marks = [
        [(1, 3)],
        [(1, 2)], 
        []
    ]

    # --- 图表初始化 ---
    fig, ax = plt.subplots(figsize=(len(categories) * 2.5, 5), dpi=300)

    # --- 计算柱子位置 ---
    x_base = np.arange(len(categories))  # 基础 X 坐标：[0, 1, 2]
    total_width = 0.7  # 簇的总宽度

    for index, category in enumerate(categories):
        means = all_means[index]
        errs = all_errs[index]
        raw_data = all_raw_data[index]

        n_subgroups = len(category[1])
        bar_width = total_width / n_subgroups

        offsets = np.linspace(
            -total_width / 2 + bar_width / 2, 
            total_width / 2 - bar_width / 2, 
            n_subgroups
        )

        colors = generate_prism_colors(n_subgroups)
        
        all_x_positions = []
        for i in range(n_subgroups):
            x_current: float = x_base[index] + offsets[i]
            all_x_positions.append(x_current)

            asymmetric_errs = [errs[i]]
            ax.bar(x_current, means[i], yerr=asymmetric_errs, width=bar_width,
               label=category[1][i], color=colors[i], edgecolor='black', linewidth=1.5, alpha=0.8,
               capsize=5, error_kw={'elinewidth': 1.2, 'capthick': 1.2})

        for i, data in enumerate(raw_data):
            x_jittered = generate_jittered_x(data, r_x=0.02, r_y=30) + all_x_positions[i]
            ax.scatter(x_jittered, data, 
                    color='white',            # 散点内部填充白色
                    edgecolor='black',        # 散点黑色描边
                    alpha=0.75,                # 散点透明度
                    s=20,                     # 散点大小
                    zorder=3)                 # 确保散点图层在柱子上方

        
        target_index = []
        curr_stars_mark = stars_marks[index]
        stars_list = []
        for item in curr_stars_mark:
            target_index.append(item[0])
            stars_list.append(item[1])

        draw_stars(
            ax,
            target_index,
            all_x_positions,
            stars_list,
            raw_data,
            means,
            errs
        )

    # --- 格式化设置 ---
    categories_name = [group[0] for group in categories]
    ax.set_xticks(x_base)
    ax.set_xticklabels(categories_name)
    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=15)

    # --- 保存图表 ---
    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / img_name

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()