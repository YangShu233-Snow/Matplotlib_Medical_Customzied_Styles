from __future__ import annotations

from typing import Literal

import numpy as np

BandwidthMethod = Literal["scott", "silverman"]


def calculate_bandwidth(data: np.ndarray, method: BandwidthMethod = "scott") -> float:
    n = len(data)
    sigma = np.std(data, ddof=1)
    if method == "scott":
        return float(sigma * (n ** (-1 / 5)))
    if method == "silverman":
        iqr = float(np.subtract(*np.percentile(data, [75, 25])))
        A = min(sigma, iqr / 1.34)
        return float(0.9 * A * (n ** (-1 / 5)))
    msg = f"Unknown bandwidth method: {method}"
    raise ValueError(msg)


def significance_stars(p_value: float) -> str:
    if p_value <= 0.0001:
        return "****"
    if p_value <= 0.001:
        return "***"
    if p_value <= 0.01:
        return "**"
    if p_value <= 0.05:
        return "*"
    return "ns"
