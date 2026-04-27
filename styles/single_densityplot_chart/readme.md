# 单组/对比密度图 - GraphPad 风格 (Single Density Plot Chart GraphPad Style)

这是一个用于绘制具有专业学术审美风格的密度分布图 (Density Plot) 的示例，旨在复刻 GraphPad Prism 等软件的平滑曲线与半透明填充效果。

## 📊 效果预览

![](img/example.png)

## ✨ 核心特性

*   **智能带宽校正**：内置 `calculate_bandwidth` 函数，内置 Scott 和 Silverman 规则。
*   **GraphPad 审美预设**：通过 `assets/single_densityplot_chart.mplstyle` 全局定义了加粗的坐标轴、无边框图例以及符合学术规范的 4 色配色循环。
*   **轮廓与填充结合**：代码演示了如何同时使用 `ax.plot` (轮廓线) 与 `ax.fill_between` (半透明填充) 来增强视觉对比。可通过 `filled_with_color: bool = True` 控制是否启用填充。
*   **自动收口优化**：绘图逻辑会自动在数据极值两侧预留 40% 的余量，确保密度曲线能够自然、平滑地降至零点。

## 🚀 快速运行

确保你已经激活了 Conda 环境。然后在当前目录下运行：

```bash
python example.py
```

运行后，图表将自动生成并保存在 `./img/` 文件夹下。

## 🛠️ 如何替换为你自己的数据？

打开 `example.py`，在 `main` 函数中调整数据：

```python
# 1. 设置标签与标题
xlabel = 'Your X Label'
ylabel = 'Density'
labels = ['Group 1', 'Group 2']

# 2. 传入你的 NumPy 数组
all_data = [
    np.array([...]), # 数据组 1
    np.array([...])  # 数据组 2
]

# 3. 选择平滑算法
bandwidth_algorithm = 'scott' # 或 'silverman'

# 4. (可选) 关闭曲线下方填充
filled_with_color = False
```
