"""Chemical equilibrium helpers."""

from __future__ import annotations

import math


def scale_equilibrium_287(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_288(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_289(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_290(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_291(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_292(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_293(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_294(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_295(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_296(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_297(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_298(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_299(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_300(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_301(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_302(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_303(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_304(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_305(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_306(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_307(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_308(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_309(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_310(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_311(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_312(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_313(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_314(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_315(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_316(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_317(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_318(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_319(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_320(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_321(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_322(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_323(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_324(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_325(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_326(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_327(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_328(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_329(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_330(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_331(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_332(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_333(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_334(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_335(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_336(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_337(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_338(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_339(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_340(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_341(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_342(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_343(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_344(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_345(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_346(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_347(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_348(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_349(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_350(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_351(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_352(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_353(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_354(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_355(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_356(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_357(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_358(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_359(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_360(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_361(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_362(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_363(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_364(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_365(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_366(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_367(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_368(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_369(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_370(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_371(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_372(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_373(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_374(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_375(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_376(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_377(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_378(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_379(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_380(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_equilibrium_381(value: float, low: float, high: float) -> float:
    """Clamp a equilibrium value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_equilibrium_382(values: list[float], factor: float) -> list[float]:
    """Multiply every equilibrium value by the same factor."""
    return [value * factor for value in values]


def relative_change_equilibrium_383(before: float, after: float) -> float:
    """Relative change of a equilibrium quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_equilibrium_384(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced equilibrium samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_equilibrium_385(samples: list[float]) -> float:
    """Arithmetic mean of the equilibrium samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)
