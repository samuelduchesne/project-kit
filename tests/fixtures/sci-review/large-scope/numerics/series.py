"""Series helpers."""

from __future__ import annotations

import math


def trapezoid_series_1079(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1080(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1081(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1082(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1083(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1084(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1085(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1086(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1087(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1088(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1089(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1090(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1091(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1092(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1093(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1094(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1095(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1096(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1097(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1098(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1099(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1100(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1101(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1102(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1103(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1104(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1105(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1106(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1107(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1108(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1109(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1110(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1111(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1112(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1113(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1114(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1115(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1116(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1117(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1118(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1119(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1120(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1121(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1122(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1123(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1124(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1125(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1126(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1127(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1128(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1129(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1130(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1131(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1132(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1133(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1134(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1135(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1136(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1137(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1138(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1139(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1140(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1141(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1142(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1143(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1144(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1145(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1146(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1147(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1148(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1149(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1150(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1151(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1152(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1153(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1154(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1155(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1156(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1157(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1158(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1159(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1160(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1161(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1162(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1163(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1164(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1165(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1166(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1167(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1168(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1169(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1170(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1171(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1172(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]


def relative_change_series_1173(before: float, after: float) -> float:
    """Relative change of a series quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_series_1174(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced series samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_series_1175(samples: list[float]) -> float:
    """Arithmetic mean of the series samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_series_1176(value: float, low: float, high: float) -> float:
    """Clamp a series value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_series_1177(values: list[float], factor: float) -> list[float]:
    """Multiply every series value by the same factor."""
    return [value * factor for value in values]
