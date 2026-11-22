"""Reproduction check for py-euler-step-count-drift.

One day of hourly steps (step 1/24 day) must give 24 steps, a trajectory of
25 points ending at t = 1 day.
"""

from _common import failed, passed, setup

setup()
from limno.ecology import euler_run  # noqa: E402

trajectory = euler_run(lambda t, y: [0.0], [1.0], 1.0, 1.0 / 24.0)
steps = len(trajectory) - 1
end = trajectory[-1][0]
if steps != 24 or abs(end - 1.0) > 1e-9:
    failed(f"one day of hourly steps takes {steps} steps and ends at t = {end!r} days; expected 24 steps ending at 1")
passed(f"{steps} steps ending at {end}")
