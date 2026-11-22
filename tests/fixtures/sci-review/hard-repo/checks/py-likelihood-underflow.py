"""Reproduction check for py-likelihood-underflow.

Two years of hourly residuals (17520 values) alternating between +0.5 and
-0.5 K with sigma 0.5 K have the log-likelihood
-n * (log(sigma * sqrt(2 pi)) + 0.5) = -12715.9.
"""

import math

from _common import failed, passed, setup

setup()
from limno.calibrate import gaussian_log_likelihood  # noqa: E402

n = 17520
residuals = [0.5 if i % 2 == 0 else -0.5 for i in range(n)]
expected = -n * (math.log(0.5 * math.sqrt(2.0 * math.pi)) + 0.5)
try:
    value = gaussian_log_likelihood(residuals, 0.5)
except (ValueError, OverflowError) as error:
    failed(f"log-likelihood of {n} residuals raises {type(error).__name__}: {error}; expected {expected:.1f}")
if not math.isfinite(value) or abs(value - expected) > 1e-6 * abs(expected):
    failed(f"log-likelihood {value} for {n} residuals; expected {expected:.1f}")
passed(f"log-likelihood {value:.1f}")
