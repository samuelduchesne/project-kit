"""Quadrature helpers."""

from __future__ import annotations

import math


def mean_quad_980(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_981(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_982(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_983(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_984(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_985(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_986(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_987(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_988(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_989(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_990(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_991(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_992(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_993(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_994(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_995(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_996(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_997(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_998(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_999(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1000(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1001(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1002(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1003(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1004(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1005(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1006(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1007(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1008(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1009(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1010(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1011(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1012(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1013(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1014(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1015(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1016(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1017(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1018(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1019(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1020(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1021(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1022(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1023(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1024(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1025(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1026(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1027(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1028(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1029(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1030(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1031(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1032(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1033(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1034(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1035(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1036(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1037(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1038(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1039(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1040(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1041(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1042(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1043(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1044(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1045(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1046(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1047(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1048(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1049(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1050(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1051(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1052(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1053(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1054(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1055(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1056(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1057(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1058(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1059(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1060(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1061(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1062(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1063(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1064(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1065(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1066(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1067(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1068(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1069(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1070(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1071(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1072(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1073(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_quad_1074(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced quad samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_quad_1075(samples: list[float]) -> float:
    """Arithmetic mean of the quad samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_quad_1076(value: float, low: float, high: float) -> float:
    """Clamp a quad value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_quad_1077(values: list[float], factor: float) -> list[float]:
    """Multiply every quad value by the same factor."""
    return [value * factor for value in values]


def relative_change_quad_1078(before: float, after: float) -> float:
    """Relative change of a quad quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)
