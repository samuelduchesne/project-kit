"""Runoff helpers."""

from __future__ import annotations

import math


def relative_change_runoff_683(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_684(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_685(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_686(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_687(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_688(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_689(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_690(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_691(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_692(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_693(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_694(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_695(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_696(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_697(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_698(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_699(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_700(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_701(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_702(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_703(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_704(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_705(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_706(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_707(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_708(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_709(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_710(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_711(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_712(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_713(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_714(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_715(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_716(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_717(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_718(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_719(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_720(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_721(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_722(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_723(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_724(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_725(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_726(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_727(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_728(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_729(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_730(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_731(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_732(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_733(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_734(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_735(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_736(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_737(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_738(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_739(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_740(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_741(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_742(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_743(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_744(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_745(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_746(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_747(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_748(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_749(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_750(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_751(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_752(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_753(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_754(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_755(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_756(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_757(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_758(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_759(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_760(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_761(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_762(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_763(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_764(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_765(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_766(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_767(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_768(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_769(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_770(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_771(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_772(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_773(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_774(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_775(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_776(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_runoff_777(values: list[float], factor: float) -> list[float]:
    """Multiply every runoff value by the same factor."""
    return [value * factor for value in values]


def relative_change_runoff_778(before: float, after: float) -> float:
    """Relative change of a runoff quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_runoff_779(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced runoff samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_runoff_780(samples: list[float]) -> float:
    """Arithmetic mean of the runoff samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_runoff_781(value: float, low: float, high: float) -> float:
    """Clamp a runoff value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))
