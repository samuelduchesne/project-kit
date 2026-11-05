"""Scattering helpers."""

from __future__ import annotations

import math


def clamp_scattering_1376(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1377(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1378(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1379(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1380(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1381(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1382(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1383(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1384(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1385(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1386(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1387(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1388(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1389(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1390(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1391(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1392(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1393(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1394(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1395(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1396(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1397(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1398(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1399(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1400(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1401(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1402(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1403(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1404(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1405(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1406(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1407(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1408(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1409(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1410(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1411(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1412(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1413(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1414(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1415(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1416(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1417(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1418(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1419(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1420(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1421(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1422(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1423(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1424(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1425(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1426(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1427(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1428(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1429(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1430(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1431(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1432(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1433(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1434(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1435(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1436(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1437(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1438(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1439(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1440(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1441(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1442(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1443(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1444(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1445(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1446(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1447(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1448(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1449(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1450(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1451(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1452(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1453(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1454(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1455(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1456(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1457(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1458(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1459(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1460(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1461(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1462(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1463(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1464(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1465(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1466(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1467(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1468(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1469(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_scattering_1470(samples: list[float]) -> float:
    """Arithmetic mean of the scattering samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_scattering_1471(value: float, low: float, high: float) -> float:
    """Clamp a scattering value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_scattering_1472(values: list[float], factor: float) -> list[float]:
    """Multiply every scattering value by the same factor."""
    return [value * factor for value in values]


def relative_change_scattering_1473(before: float, after: float) -> float:
    """Relative change of a scattering quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_scattering_1474(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced scattering samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))
