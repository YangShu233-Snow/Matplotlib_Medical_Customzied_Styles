import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

import mmcs
from mmcs import Style
from mmcs.charts import bar


@pytest.mark.mpl_image_compare
def test_bar_graphpad():
    np.random.seed(12)
    result = mmcs.bar_chart(
        [1200, 3500], groups=["Control", "KO"],
        errors=[300, 400], stars=[0, 3],
    )
    return result.fig


@pytest.mark.mpl_image_compare
def test_bar_multi_graphpad():
    np.random.seed(12)
    style = Style("graphpad_prism")
    style.apply(plt.rcParams, chart_type="bar")
    fig, axs = plt.subplots(1, 2, figsize=(8, 4))
    plt.subplots_adjust(wspace=0.8)

    datasets = [
        (["Con", "KO"], [1200, 3500], [300, 400], [0, 3]),
        (["WT", "Mut"], [800, 2200], [200, 300], [0, 4]),
    ]
    for ax, (groups, means, errs, stars) in zip(axs, datasets):
        bar.render(ax, means, groups=groups, errors=errs, stars=stars)
        ax.set_ylabel("Value")
    fig.tight_layout()
    return fig


@pytest.mark.mpl_image_compare
def test_boxplot_graphpad():
    np.random.seed(12)
    data = [
        np.random.normal(500, 150, 40),
        np.random.normal(900, 100, 40),
        np.random.normal(380, 80, 40),
    ]
    result = mmcs.box_chart(data, groups=["Sample A", "Sample B", "Sample C"])
    return result.fig


@pytest.mark.mpl_image_compare
def test_scatter_graphpad():
    np.random.seed(12)
    x = np.concatenate([np.random.normal(50, 10, 50), np.random.normal(500, 100, 50)])
    y = np.concatenate([np.random.normal(600, 200, 50), np.random.normal(60, 10, 50)])
    result = mmcs.scatter_chart(x, y)
    return result.fig


@pytest.mark.mpl_image_compare
def test_violin_graphpad():
    np.random.seed(12)
    data = [
        np.random.normal(200, 80, 200),
        np.random.normal(800, 500, 200),
        np.random.normal(600, 100, 200),
    ]
    result = mmcs.violin_chart(data, groups=[f"Sample {i+1}" for i in range(3)])
    return result.fig


@pytest.mark.mpl_image_compare
def test_histogram_graphpad():
    np.random.seed(12)
    data = np.random.normal(loc=50, scale=10, size=1000)
    result = mmcs.histogram_chart(data)
    return result.fig


@pytest.mark.mpl_image_compare
def test_density_graphpad():
    np.random.seed(42)
    data = [
        np.random.normal(100, 20, 200),
        np.random.normal(130, 25, 200),
    ]
    result = mmcs.density_chart(data, groups=["Control", "Treatment"])
    return result.fig


@pytest.mark.mpl_image_compare
def test_regression_graphpad():
    np.random.seed(12)
    x = np.random.uniform(3, 10, size=50)
    y = x + np.random.uniform(-2, 4, size=50)
    result = mmcs.regression_chart(x, y)
    return result.fig


@pytest.mark.mpl_image_compare
def test_clustered_scatter_graphpad():
    np.random.seed(12)
    x = np.concatenate([np.random.normal(50, 10, 50), np.random.normal(500, 100, 50)])
    y = np.concatenate([np.random.normal(600, 200, 50), np.random.normal(60, 10, 50)])
    result = mmcs.scatter_clustered_chart(x, y)
    return result.fig
