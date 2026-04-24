import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/single_boxplot_chart.mplstyle'
plt.style.use(style_file)

def main():
    # --- config ---
    title = 'Title'
    ylabel = 'Value'
    img_name = 'example'
    
    show_mean = True
    is_notch = False

    # 模拟数据
    np.random.seed(12)
    data = [
        np.random.normal(500, 150, 40),
        np.random.normal(900, 100, 40),
        np.random.normal(380, 80, 40)
    ]

    labels = [f'Sample_{index+1}' for index in range(len(data))]

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.boxplot(
        data,
        tick_labels=labels,
        notch=is_notch,
        showmeans=show_mean,
        patch_artist=True,
        boxprops=dict(facecolor='#CCCCCC')
    )

    ax.set_title(title)
    ax.set_ylabel(ylabel)

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
