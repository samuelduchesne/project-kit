"""Infiltration helpers."""

from __future__ import annotations

import math


def trapezoid_infiltration_584(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_585(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_586(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_587(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_588(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_589(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_590(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_591(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_592(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_593(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_594(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_595(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_596(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_597(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_598(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_599(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_600(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_601(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_602(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_603(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_604(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_605(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_606(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_607(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_608(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_609(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_610(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_611(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_612(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_613(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_614(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_615(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_616(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_617(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_618(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_619(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_620(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_621(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_622(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_623(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_624(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_625(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_626(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_627(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_628(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_629(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_630(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_631(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_632(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_633(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_634(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_635(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_636(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_637(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_638(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_639(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_640(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_641(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_642(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_643(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_644(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_645(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_646(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_647(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_648(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_649(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_650(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_651(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_652(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_653(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_654(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_655(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_656(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_657(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_658(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_659(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_660(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_661(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_662(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_663(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_664(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_665(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_666(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_667(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_668(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_669(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_670(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_671(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_672(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_673(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_674(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_675(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_676(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_677(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]


def relative_change_infiltration_678(before: float, after: float) -> float:
    """Relative change of a infiltration quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_infiltration_679(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced infiltration samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_infiltration_680(samples: list[float]) -> float:
    """Arithmetic mean of the infiltration samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_infiltration_681(value: float, low: float, high: float) -> float:
    """Clamp a infiltration value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_infiltration_682(values: list[float], factor: float) -> list[float]:
    """Multiply every infiltration value by the same factor."""
    return [value * factor for value in values]
