"""Reaction kinetics helpers."""

from __future__ import annotations

import math


def clamp_kinetics_386(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_387(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_388(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_389(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_390(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_391(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_392(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_393(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_394(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_395(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_396(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_397(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_398(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_399(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_400(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_401(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_402(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_403(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_404(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_405(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_406(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_407(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_408(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_409(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_410(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_411(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_412(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_413(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_414(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_415(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_416(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_417(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_418(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_419(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_420(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_421(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_422(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_423(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_424(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_425(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_426(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_427(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_428(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_429(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_430(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_431(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_432(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_433(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_434(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_435(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_436(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_437(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_438(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_439(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_440(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_441(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_442(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_443(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_444(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_445(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_446(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_447(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_448(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_449(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_450(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_451(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_452(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_453(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_454(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_455(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_456(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_457(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_458(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_459(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_460(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_461(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_462(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_463(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_464(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_465(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_466(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_467(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_468(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_469(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_470(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_471(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_472(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_473(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_474(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_475(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_476(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_477(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_478(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_479(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kinetics_480(samples: list[float]) -> float:
    """Arithmetic mean of the kinetics samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kinetics_481(value: float, low: float, high: float) -> float:
    """Clamp a kinetics value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kinetics_482(values: list[float], factor: float) -> list[float]:
    """Multiply every kinetics value by the same factor."""
    return [value * factor for value in values]


def relative_change_kinetics_483(before: float, after: float) -> float:
    """Relative change of a kinetics quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kinetics_484(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kinetics samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))
