import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path

root_path = Path(__file__).parent
# 修改为要求的样式文件路径
style_file = root_path / './assets/single_volinplot_chart.mplstyle'
plt.style.use(style_file)

def main():
    # --- config ---
    title = 'Title'
    ylabel = 'value'
    img_name = 'example'

    np.random.seed(12)
    

    save_dir = root_path / Path('./img')
    save_dir.mkdir(parents=True, exist_ok=True)
    save_paths = [save_dir / f"{img_name}.png", save_dir / f"{img_name}.pdf"]

    plt.tight_layout()
    for save_path in save_paths:
        plt.savefig(save_path, bbox_inches='tight')

if __name__ == '__main__':
    main()
