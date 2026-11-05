"""Interpolation helpers."""

from __future__ import annotations

import math


def clamp_interp_881(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_882(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_883(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_884(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_885(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_886(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_887(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_888(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_889(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_890(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_891(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_892(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_893(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_894(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_895(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_896(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_897(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_898(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_899(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_900(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_901(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_902(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_903(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_904(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_905(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_906(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_907(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_908(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_909(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_910(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_911(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_912(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_913(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_914(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_915(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_916(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_917(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_918(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_919(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_920(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_921(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_922(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_923(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_924(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_925(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_926(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_927(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_928(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_929(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_930(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_931(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_932(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_933(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_934(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_935(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_936(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_937(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_938(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_939(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_940(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_941(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_942(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_943(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_944(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_945(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_946(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_947(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_948(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_949(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_950(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_951(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_952(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_953(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_954(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_955(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_956(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_957(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_958(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_959(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_960(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_961(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_962(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_963(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_964(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_965(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_966(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_967(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_968(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_969(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_970(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_971(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_972(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_973(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_974(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_interp_975(samples: list[float]) -> float:
    """Arithmetic mean of the interp samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_interp_976(value: float, low: float, high: float) -> float:
    """Clamp a interp value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_interp_977(values: list[float], factor: float) -> list[float]:
    """Multiply every interp value by the same factor."""
    return [value * factor for value in values]


def relative_change_interp_978(before: float, after: float) -> float:
    """Relative change of a interp quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_interp_979(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced interp samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))
