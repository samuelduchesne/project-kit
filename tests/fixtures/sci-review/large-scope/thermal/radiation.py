"""Thermal radiation helpers."""

from __future__ import annotations

import math


def trapezoid_thermal_radiation_2274(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2275(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2276(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2277(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2278(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2279(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2280(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2281(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2282(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2283(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2284(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2285(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2286(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2287(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2288(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2289(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2290(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2291(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2292(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2293(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2294(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2295(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2296(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2297(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2298(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2299(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2300(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2301(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2302(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2303(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2304(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2305(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2306(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2307(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2308(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2309(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2310(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2311(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2312(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2313(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2314(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2315(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2316(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2317(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2318(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2319(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2320(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2321(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2322(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2323(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2324(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2325(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2326(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2327(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2328(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2329(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2330(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2331(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2332(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2333(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2334(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2335(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2336(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2337(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2338(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2339(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2340(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2341(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2342(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2343(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2344(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2345(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2346(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2347(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2348(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2349(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2350(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2351(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2352(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2353(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2354(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2355(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2356(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2357(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2358(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2359(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2360(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2361(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2362(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2363(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2364(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2365(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2366(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2367(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_thermal_radiation_2368(before: float, after: float) -> float:
    """Relative change of a thermal_radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_thermal_radiation_2369(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced thermal_radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_thermal_radiation_2370(samples: list[float]) -> float:
    """Arithmetic mean of the thermal_radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_thermal_radiation_2371(value: float, low: float, high: float) -> float:
    """Clamp a thermal_radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_thermal_radiation_2372(values: list[float], factor: float) -> list[float]:
    """Multiply every thermal_radiation value by the same factor."""
    return [value * factor for value in values]
