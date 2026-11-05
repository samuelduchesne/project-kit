"""Area conversions."""

from __future__ import annotations

import math


def relative_change_area_2373(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2374(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2375(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2376(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2377(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2378(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2379(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2380(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2381(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2382(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2383(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2384(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2385(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2386(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2387(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2388(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2389(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2390(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2391(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2392(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2393(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2394(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2395(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2396(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2397(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2398(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2399(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2400(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2401(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2402(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2403(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2404(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2405(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2406(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2407(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2408(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2409(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2410(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2411(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2412(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2413(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2414(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2415(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2416(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2417(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2418(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2419(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2420(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2421(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2422(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2423(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2424(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2425(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2426(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2427(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2428(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2429(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2430(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2431(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2432(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2433(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2434(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2435(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2436(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2437(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2438(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2439(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2440(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2441(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2442(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2443(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2444(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2445(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2446(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2447(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2448(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2449(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2450(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2451(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2452(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2453(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2454(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2455(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2456(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2457(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2458(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2459(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2460(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2461(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2462(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2463(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2464(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2465(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2466(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_area_2467(values: list[float], factor: float) -> list[float]:
    """Multiply every area value by the same factor."""
    return [value * factor for value in values]


def relative_change_area_2468(before: float, after: float) -> float:
    """Relative change of a area quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_area_2469(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced area samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_area_2470(samples: list[float]) -> float:
    """Arithmetic mean of the area samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_area_2471(value: float, low: float, high: float) -> float:
    """Clamp a area value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))
