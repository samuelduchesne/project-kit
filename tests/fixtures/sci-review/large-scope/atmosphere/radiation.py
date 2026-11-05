"""Radiation helpers."""

from __future__ import annotations

import math


def clamp_radiation_96(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_97(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_98(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_99(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_100(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_101(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_102(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_103(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_104(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_105(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_106(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_107(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_108(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_109(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_110(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_111(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_112(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_113(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_114(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_115(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_116(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_117(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_118(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_119(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_120(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_121(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_122(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_123(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_124(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_125(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_126(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_127(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_128(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_129(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_130(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_131(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_132(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_133(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_134(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_135(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_136(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_137(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_138(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_139(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_140(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_141(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_142(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_143(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_144(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_145(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_146(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_147(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_148(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_149(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_150(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_151(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_152(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_153(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_154(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_155(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_156(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_157(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_158(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_159(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_160(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_161(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_162(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_163(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_164(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_165(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_166(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_167(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_168(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_169(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_170(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_171(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_172(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_173(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_174(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_175(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_176(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_177(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_178(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_179(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_180(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_181(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_182(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_183(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_184(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_185(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_186(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def scale_radiation_187(values: list[float], factor: float) -> list[float]:
    """Multiply every radiation value by the same factor."""
    return [value * factor for value in values]


def relative_change_radiation_188(before: float, after: float) -> float:
    """Relative change of a radiation quantity, (after - before) / |before|."""
    if before == 0.0:
        raise ZeroDivisionError("relative change from zero is undefined")
    return (after - before) / abs(before)


def trapezoid_radiation_189(y: list[float], dx: float) -> float:
    """Composite trapezoidal integral of equally spaced radiation samples."""
    if len(y) < 2:
        return 0.0
    return dx * (math.fsum(y) - 0.5 * (y[0] + y[-1]))


def mean_radiation_190(samples: list[float]) -> float:
    """Arithmetic mean of the radiation samples; 0.0 for an empty list."""
    if not samples:
        return 0.0
    return math.fsum(samples) / len(samples)


def clamp_radiation_191(value: float, low: float, high: float) -> float:
    """Clamp a radiation value to the closed interval [low, high]."""
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))
