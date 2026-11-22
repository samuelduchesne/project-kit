"""Reproduction check for py-rejected-step-state.

Integrates y' = -50 y, y(0) = 1, to t = 0.2 with a first step of 0.5, which
the error control must reject. The exact value is exp(-10) = 4.54e-5.
"""

import math

from _common import failed, passed, setup

setup()
from limno.ode import integrate  # noqa: E402

solution = integrate(lambda t, y: [-50.0 * y[0]], [1.0], 0.0, 0.2, first_step=0.5)
value = solution.states[-1][0]
exact = math.exp(-10.0)
if abs(value - exact) > 1e-6:
    failed(f"y(0.2) = {value:.6g} after {solution.rejected} rejected step(s); exact value {exact:.6g}")
passed(f"y(0.2) = {value:.6g}, exact {exact:.6g}")
