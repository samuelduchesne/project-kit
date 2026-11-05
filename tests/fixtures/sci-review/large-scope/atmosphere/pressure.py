"""Pressure helpers."""

from __future__ import annotations

import math


def mean_pressure_0(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_1(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_2(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_3(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_4(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_5(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_6(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_7(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_8(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_9(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_10(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_11(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_12(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_13(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_14(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_15(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_16(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_17(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_18(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_19(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_20(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_21(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_22(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_23(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_24(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_25(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_26(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_27(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_28(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_29(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_30(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_31(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_32(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_33(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_34(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_35(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_36(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_37(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_38(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_39(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_40(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_41(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_42(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_43(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_44(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_45(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_46(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_47(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_48(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_49(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_50(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_51(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_52(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_53(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_54(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_55(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_56(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_57(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_58(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_59(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_60(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_61(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_62(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_63(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_64(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_65(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_66(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_67(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_68(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_69(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_70(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_71(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_72(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_73(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_74(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_75(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_76(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_77(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_78(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_79(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_80(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_81(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_82(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_83(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_84(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_85(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_86(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_87(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_88(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_89(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_90(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_pressure_91(value: float, low: float, high: float) -> float:
    """Clamp a pressure value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_pressure_92(values: list[float], factor: float) -> list[float]:
    """Multiply every pressure value by the same factor."""
    return [value * factor for value in values]


def relative_change_pressure_93(before: float, after: float) -> float:
    """Relative change of a pressure quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_pressure_94(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced pressure samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_pressure_95(samples: list[float]) -> float:
    """Arithmetic mean of the pressure samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)
