"""Reproduction check for py-light-limitation-closed-form.

Compares the closed form of the depth-averaged light limitation with a fine
midpoint quadrature of I(z) / (I(z) + K), I(z) = I0 exp(-k z), over [0, H].
"""

import math

from _common import failed, passed, setup

setup()
from limno.ecology import mean_light_limitation  # noqa: E402

i0, k_half, k, depth = 200.0, 40.0, 0.3, 10.0
steps = 20000
dz = depth / steps
reference = 0.0
for j in range(steps):
    light = i0 * math.exp(-k * (j + 0.5) * dz)
    reference += light / (light + k_half) * dz
reference /= depth
value = mean_light_limitation(i0, k_half, k, depth)
if abs(value - reference) > 1e-6:
    failed(f"mean limitation {value:.5f} for I0=200, K=40, k=0.3, H=10; quadrature gives {reference:.5f}")
passed(f"mean limitation {value:.5f} matches quadrature {reference:.5f}")
