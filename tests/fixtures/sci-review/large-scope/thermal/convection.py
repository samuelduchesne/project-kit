"""Convection helpers."""

from __future__ import annotations

import math


def mean_convection_2175(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2176(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2177(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2178(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2179(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2180(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2181(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2182(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2183(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2184(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2185(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2186(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2187(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2188(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2189(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2190(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2191(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2192(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2193(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2194(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2195(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2196(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2197(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2198(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2199(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2200(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2201(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2202(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2203(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2204(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2205(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2206(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2207(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2208(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2209(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2210(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2211(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2212(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2213(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2214(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2215(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2216(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2217(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2218(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2219(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2220(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2221(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2222(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2223(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2224(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2225(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2226(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2227(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2228(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2229(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2230(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2231(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2232(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2233(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2234(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2235(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2236(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2237(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2238(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2239(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2240(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2241(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2242(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2243(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2244(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2245(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2246(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2247(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2248(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2249(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2250(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2251(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2252(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2253(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2254(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2255(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2256(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2257(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2258(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2259(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2260(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2261(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2262(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2263(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2264(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2265(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2266(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2267(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2268(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_convection_2269(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced convection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_convection_2270(samples: list[float]) -> float:
    """Arithmetic mean of the convection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_convection_2271(value: float, low: float, high: float) -> float:
    """Clamp a convection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_convection_2272(values: list[float], factor: float) -> list[float]:
    """Multiply every convection value by the same factor."""
    return [value * factor for value in values]


def relative_change_convection_2273(before: float, after: float) -> float:
    """Relative change of a convection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)
