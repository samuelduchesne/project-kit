"""Unit conversions for heat flow reports."""

from __future__ import annotations

import math


def clamp_units_2571(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2572(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2573(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2574(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2575(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2576(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2577(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2578(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2579(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2580(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2581(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2582(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2583(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2584(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2585(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2586(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2587(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2588(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2589(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2590(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2591(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2592(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2593(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2594(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2595(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2596(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2597(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2598(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2599(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2600(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2601(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2602(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2603(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2604(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2605(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2606(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2607(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2608(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2609(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2610(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2611(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2612(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2613(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2614(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2615(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2616(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2617(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2618(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2619(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2620(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2621(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2622(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2623(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2624(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2625(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2626(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2627(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2628(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2629(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2630(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2631(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2632(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2633(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2634(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2635(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2636(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2637(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2638(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2639(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2640(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2641(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2642(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2643(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2644(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2645(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2646(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2647(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2648(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2649(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2650(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2651(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2652(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2653(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2654(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2655(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2656(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2657(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2658(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2659(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2660(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2661(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_units_2662(values: list[float], factor: float) -> list[float]:
    """Multiply every units value by the same factor."""
    return [value * factor for value in values]


def relative_change_units_2663(before: float, after: float) -> float:
    """Relative change of a units quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_units_2664(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced units samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_units_2665(samples: list[float]) -> float:
    """Arithmetic mean of the units samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_units_2666(value: float, low: float, high: float) -> float:
    """Clamp a units value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


WATTS_PER_BTU_PER_HOUR = 0.29307107


def btu_per_hour_to_watts(heat_flow_btu_per_hour: float) -> float:
    """Convert a heat flow from BTU/h to W."""
    return heat_flow_btu_per_hour * 3.412141633
