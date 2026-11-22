"""Reproduction check for py-ci-population-std.

The t interval of the mean of (1, 2, 3, 4, 5) has half-width
t(0.975, 4) * s / sqrt(5) = 2.776 * 1.5811 / 2.2361 = 1.963.
"""

from _common import failed, passed, setup

setup()
from limno.stats import mean_confidence_interval  # noqa: E402

low, high = mean_confidence_interval([1.0, 2.0, 3.0, 4.0, 5.0])
half = 0.5 * (high - low)
if abs(half - 1.9629) > 1e-3:
    failed(f"95% half-width {half:.4f} for (1, 2, 3, 4, 5); expected 1.9629 with the sample standard deviation")
passed(f"half-width {half:.4f}")
