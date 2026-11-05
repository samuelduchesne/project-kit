"""Solver kernels (one module larger than a review part)."""

from __future__ import annotations

import math


def mean_kernel_1475(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1476(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1477(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1478(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1479(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1480(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1481(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1482(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1483(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1484(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1485(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1486(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1487(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1488(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1489(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1490(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1491(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1492(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1493(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1494(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1495(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1496(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1497(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1498(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1499(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1500(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1501(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1502(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1503(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1504(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1505(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1506(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1507(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1508(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1509(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1510(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1511(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1512(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1513(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1514(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1515(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1516(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1517(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1518(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1519(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1520(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1521(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1522(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1523(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1524(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1525(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1526(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1527(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1528(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1529(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1530(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1531(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1532(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1533(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1534(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1535(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1536(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1537(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1538(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1539(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1540(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1541(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1542(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1543(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1544(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1545(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1546(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1547(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1548(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1549(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1550(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1551(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1552(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1553(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1554(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1555(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1556(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1557(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1558(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1559(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1560(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1561(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1562(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1563(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1564(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1565(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1566(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1567(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1568(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1569(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1570(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1571(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1572(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1573(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1574(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1575(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1576(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1577(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1578(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1579(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1580(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1581(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1582(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1583(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1584(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1585(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1586(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1587(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1588(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1589(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1590(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1591(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1592(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1593(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1594(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1595(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1596(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1597(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1598(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1599(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1600(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1601(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1602(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1603(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1604(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1605(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1606(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1607(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1608(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1609(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1610(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1611(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1612(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1613(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1614(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1615(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1616(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1617(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1618(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1619(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1620(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1621(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1622(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1623(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1624(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1625(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1626(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1627(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1628(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1629(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1630(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1631(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1632(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1633(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1634(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1635(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1636(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1637(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1638(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1639(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1640(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1641(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1642(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1643(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1644(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1645(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1646(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1647(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1648(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1649(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1650(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1651(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1652(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1653(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1654(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1655(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1656(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1657(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1658(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1659(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1660(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1661(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1662(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1663(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1664(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1665(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1666(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1667(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1668(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1669(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1670(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1671(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1672(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1673(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1674(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1675(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1676(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1677(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1678(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1679(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1680(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1681(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1682(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1683(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1684(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1685(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1686(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1687(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1688(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1689(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1690(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1691(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1692(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1693(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1694(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1695(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1696(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1697(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1698(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1699(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1700(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1701(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1702(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1703(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1704(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1705(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1706(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1707(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1708(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1709(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1710(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1711(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1712(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1713(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1714(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1715(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1716(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1717(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1718(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1719(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1720(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1721(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1722(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1723(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1724(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1725(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1726(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1727(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1728(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1729(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1730(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1731(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1732(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1733(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1734(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1735(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1736(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1737(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1738(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1739(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1740(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1741(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1742(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1743(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1744(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1745(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1746(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1747(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1748(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1749(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1750(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1751(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1752(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1753(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1754(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1755(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1756(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1757(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1758(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1759(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1760(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1761(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1762(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1763(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1764(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1765(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1766(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1767(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1768(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1769(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1770(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1771(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1772(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1773(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1774(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1775(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1776(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1777(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1778(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1779(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1780(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1781(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1782(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1783(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1784(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1785(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1786(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1787(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1788(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1789(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1790(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1791(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1792(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1793(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1794(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1795(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1796(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1797(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1798(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1799(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1800(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1801(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1802(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1803(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1804(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1805(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1806(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1807(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1808(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1809(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1810(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1811(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1812(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1813(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1814(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1815(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1816(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1817(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1818(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1819(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1820(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1821(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1822(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1823(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1824(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1825(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1826(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1827(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1828(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1829(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1830(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1831(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1832(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1833(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1834(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1835(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1836(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1837(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1838(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1839(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1840(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1841(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1842(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1843(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1844(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1845(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1846(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1847(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1848(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1849(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1850(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1851(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1852(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1853(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1854(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1855(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1856(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1857(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1858(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1859(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1860(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1861(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1862(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1863(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1864(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1865(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1866(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1867(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1868(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1869(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1870(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1871(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1872(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1873(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1874(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1875(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1876(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1877(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1878(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1879(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1880(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1881(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1882(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1883(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1884(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1885(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1886(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1887(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1888(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1889(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1890(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1891(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1892(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1893(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1894(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1895(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1896(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1897(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1898(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1899(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1900(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1901(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1902(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1903(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1904(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1905(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1906(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1907(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1908(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1909(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1910(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1911(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1912(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1913(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1914(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1915(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1916(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1917(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1918(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1919(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1920(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1921(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1922(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1923(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1924(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1925(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1926(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1927(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1928(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1929(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1930(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1931(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1932(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1933(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1934(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1935(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1936(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1937(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1938(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1939(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1940(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1941(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1942(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1943(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1944(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1945(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1946(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1947(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1948(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1949(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1950(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1951(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1952(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1953(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1954(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1955(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1956(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1957(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1958(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1959(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1960(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1961(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1962(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1963(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1964(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1965(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1966(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1967(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1968(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_kernel_1969(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced kernel samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_kernel_1970(samples: list[float]) -> float:
    """Arithmetic mean of the kernel samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_kernel_1971(value: float, low: float, high: float) -> float:
    """Clamp a kernel value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_kernel_1972(values: list[float], factor: float) -> list[float]:
    """Multiply every kernel value by the same factor."""
    return [value * factor for value in values]


def relative_change_kernel_1973(before: float, after: float) -> float:
    """Relative change of a kernel quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)
