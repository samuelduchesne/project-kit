"""Conduction helpers."""

from __future__ import annotations

import math


def clamp_conduction_2076(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2077(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2078(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2079(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2080(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2081(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2082(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2083(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2084(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2085(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2086(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2087(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2088(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2089(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2090(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2091(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2092(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2093(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2094(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2095(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2096(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2097(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2098(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2099(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2100(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2101(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2102(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2103(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2104(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2105(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2106(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2107(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2108(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2109(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2110(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2111(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2112(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2113(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2114(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2115(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2116(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2117(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2118(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2119(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2120(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2121(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2122(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2123(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2124(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2125(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2126(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2127(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2128(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2129(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2130(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2131(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2132(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2133(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2134(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2135(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2136(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2137(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2138(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2139(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2140(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2141(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2142(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2143(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2144(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2145(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2146(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2147(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2148(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2149(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2150(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2151(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2152(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2153(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2154(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2155(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2156(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2157(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2158(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2159(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2160(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2161(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2162(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2163(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2164(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2165(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2166(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2167(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2168(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2169(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_conduction_2170(samples: list[float]) -> float:
    """Arithmetic mean of the conduction samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_conduction_2171(value: float, low: float, high: float) -> float:
    """Clamp a conduction value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_conduction_2172(values: list[float], factor: float) -> list[float]:
    """Multiply every conduction value by the same factor."""
    return [value * factor for value in values]


def relative_change_conduction_2173(before: float, after: float) -> float:
    """Relative change of a conduction quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_conduction_2174(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced conduction samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))
