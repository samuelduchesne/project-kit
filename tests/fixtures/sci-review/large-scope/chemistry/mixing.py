"""Mixing helpers."""

from __future__ import annotations

import math


def mean_mixing_485(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_486(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_487(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_488(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_489(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_490(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_491(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_492(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_493(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_494(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_495(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_496(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_497(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_498(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_499(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_500(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_501(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_502(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_503(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_504(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_505(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_506(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_507(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_508(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_509(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_510(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_511(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_512(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_513(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_514(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_515(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_516(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_517(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_518(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_519(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_520(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_521(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_522(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_523(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_524(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_525(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_526(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_527(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_528(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_529(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_530(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_531(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_532(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_533(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_534(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_535(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_536(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_537(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_538(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_539(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_540(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_541(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_542(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_543(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_544(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_545(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_546(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_547(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_548(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_549(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_550(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_551(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_552(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_553(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_554(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_555(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_556(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_557(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_558(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_559(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_560(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_561(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_562(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_563(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_564(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_565(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_566(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_567(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_568(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_569(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_570(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_571(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_572(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_573(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_574(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_575(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_576(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_577(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_578(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_mixing_579(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced mixing samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_mixing_580(samples: list[float]) -> float:
    """Arithmetic mean of the mixing samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_mixing_581(value: float, low: float, high: float) -> float:
    """Clamp a mixing value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_mixing_582(values: list[float], factor: float) -> list[float]:
    """Multiply every mixing value by the same factor."""
    return [value * factor for value in values]


def relative_change_mixing_583(before: float, after: float) -> float:
    """Relative change of a mixing quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)
