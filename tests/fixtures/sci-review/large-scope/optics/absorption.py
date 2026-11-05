"""Absorption helpers."""

from __future__ import annotations

import math


def relative_change_absorption_1178(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1179(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1180(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1181(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1182(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1183(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1184(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1185(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1186(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1187(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1188(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1189(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1190(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1191(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1192(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1193(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1194(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1195(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1196(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1197(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1198(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1199(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1200(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1201(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1202(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1203(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1204(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1205(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1206(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1207(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1208(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1209(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1210(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1211(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1212(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1213(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1214(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1215(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1216(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1217(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1218(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1219(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1220(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1221(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1222(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1223(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1224(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1225(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1226(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1227(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1228(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1229(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1230(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1231(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1232(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1233(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1234(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1235(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1236(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1237(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1238(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1239(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1240(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1241(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1242(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1243(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1244(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1245(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1246(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1247(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1248(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1249(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1250(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1251(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1252(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1253(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1254(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1255(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1256(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1257(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1258(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1259(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1260(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1261(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1262(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1263(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1264(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1265(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1266(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1267(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1268(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1269(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1270(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1271(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_absorption_1272(values: list[float], factor: float) -> list[float]:
    """Multiply every absorption value by the same factor."""
    return [value * factor for value in values]


def relative_change_absorption_1273(before: float, after: float) -> float:
    """Relative change of a absorption quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_absorption_1274(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced absorption samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_absorption_1275(samples: list[float]) -> float:
    """Arithmetic mean of the absorption samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_absorption_1276(value: float, low: float, high: float) -> float:
    """Clamp a absorption value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))
