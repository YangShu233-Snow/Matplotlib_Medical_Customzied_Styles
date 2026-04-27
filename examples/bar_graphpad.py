from pathlib import Path

from mmcs import bar_chart, save_figure

root = Path(__file__).parent

result = bar_chart(
    data=[1200, 3500],
    groups=["Control", "KO"],
    errors=[300, 400],
    stars=[0, 3],
    ylabel="Value",
    title="Single Columns Chart",
)

save_figure(result.fig, root / "img", "bar_graphpad")
