"""Physical constants and their checks."""

from __future__ import annotations

import math


def scale_constants_2472(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2473(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2474(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2475(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2476(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2477(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2478(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2479(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2480(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2481(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2482(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2483(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2484(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2485(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2486(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2487(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2488(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2489(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2490(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2491(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2492(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2493(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2494(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2495(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2496(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2497(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2498(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2499(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2500(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2501(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2502(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2503(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2504(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2505(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2506(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2507(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2508(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2509(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2510(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2511(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2512(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2513(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2514(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2515(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2516(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2517(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2518(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2519(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2520(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2521(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2522(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2523(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2524(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2525(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2526(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2527(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2528(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2529(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2530(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2531(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2532(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2533(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2534(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2535(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2536(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2537(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2538(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2539(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2540(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2541(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2542(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2543(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2544(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2545(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2546(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2547(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2548(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2549(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2550(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2551(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2552(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2553(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2554(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2555(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2556(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2557(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2558(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2559(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2560(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2561(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2562(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2563(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2564(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2565(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_constants_2566(value: float, low: float, high: float) -> float:
    """Clamp a constants value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_constants_2567(values: list[float], factor: float) -> list[float]:
    """Multiply every constants value by the same factor."""
    return [value * factor for value in values]


def relative_change_constants_2568(before: float, after: float) -> float:
    """Relative change of a constants quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_constants_2569(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced constants samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_constants_2570(samples: list[float]) -> float:
    """Arithmetic mean of the constants samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)
