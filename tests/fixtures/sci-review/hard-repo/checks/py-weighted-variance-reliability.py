"""Reproduction check for py-weighted-variance-reliability.

With equal reliability weights the unbiased weighted variance equals the
ordinary sample variance, whatever the scale of the weights.
"""

import statistics

from _common import failed, passed, setup

setup()
from limno.stats import weighted_variance  # noqa: E402

values = [10.2, 10.6, 9.9, 10.4, 10.1]
expected = statistics.variance(values)
results = []
for weight in (0.25, 1.0, 4.0):
    try:
        results.append(weighted_variance(values, [weight] * len(values)))
    except ZeroDivisionError:
        results.append(float("nan"))
if any(not abs(r - expected) <= 1e-9 for r in results):
    shown = ", ".join(f"{r:.4g}" for r in results)
    failed(f"weighted variance with equal weights 0.25, 1, 4 gives {shown}; expected {expected:.4g} each time")
passed(f"weighted variance {expected:.4g} for every weight scale")
