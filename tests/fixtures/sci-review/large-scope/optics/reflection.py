"""Reflection helpers."""

from __future__ import annotations

import math


def scale_reflection_1277(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1278(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1279(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1280(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1281(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1282(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1283(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1284(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1285(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1286(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1287(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1288(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1289(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1290(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1291(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1292(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1293(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1294(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1295(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1296(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1297(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1298(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1299(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1300(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1301(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1302(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1303(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1304(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1305(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1306(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1307(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1308(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1309(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1310(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1311(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1312(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1313(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1314(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1315(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1316(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1317(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1318(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1319(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1320(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1321(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1322(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1323(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1324(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1325(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1326(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1327(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1328(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1329(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1330(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1331(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1332(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1333(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1334(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1335(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1336(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1337(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1338(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1339(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1340(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1341(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1342(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1343(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1344(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1345(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1346(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1347(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1348(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1349(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1350(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1351(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1352(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1353(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1354(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1355(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1356(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1357(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1358(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1359(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1360(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1361(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1362(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1363(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1364(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1365(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1366(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1367(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1368(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1369(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1370(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_reflection_1371(value: float, low: float, high: float) -> float:
    """Clamp a reflection value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_reflection_1372(values: list[float], factor: float) -> list[float]:
    """Multiply every reflection value by the same factor."""
    return [value * factor for value in values]


def relative_change_reflection_1373(before: float, after: float) -> float:
    """Relative change of a reflection quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_reflection_1374(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced reflection samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_reflection_1375(samples: list[float]) -> float:
    """Arithmetic mean of the reflection samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)
