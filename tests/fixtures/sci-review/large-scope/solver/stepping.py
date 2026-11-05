"""Time-stepping helpers."""

from __future__ import annotations

import math


def trapezoid_step_1974(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_1975(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_1976(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_1977(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_1978(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_1979(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_1980(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_1981(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_1982(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_1983(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_1984(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_1985(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_1986(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_1987(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_1988(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_1989(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_1990(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_1991(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_1992(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_1993(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_1994(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_1995(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_1996(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_1997(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_1998(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_1999(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2000(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2001(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2002(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2003(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2004(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2005(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2006(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2007(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2008(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2009(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2010(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2011(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2012(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2013(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2014(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2015(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2016(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2017(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2018(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2019(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2020(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2021(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2022(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2023(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2024(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2025(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2026(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2027(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2028(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2029(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2030(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2031(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2032(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2033(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2034(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2035(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2036(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2037(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2038(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2039(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2040(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2041(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2042(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2043(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2044(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2045(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2046(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2047(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2048(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2049(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2050(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2051(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2052(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2053(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2054(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2055(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2056(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2057(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2058(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2059(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2060(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2061(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2062(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2063(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2064(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2065(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2066(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2067(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2068(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2069(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2070(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_step_2071(value: float, low: float, high: float) -> float:
    """Clamp a step value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_step_2072(values: list[float], factor: float) -> list[float]:
    """Multiply every step value by the same factor."""
    return [value * factor for value in values]


def relative_change_step_2073(before: float, after: float) -> float:
    """Relative change of a step quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_step_2074(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced step samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_step_2075(samples: list[float]) -> float:
    """Arithmetic mean of the step samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)
